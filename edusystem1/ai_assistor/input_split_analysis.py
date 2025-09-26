import json
import os
import dashscope
import numpy as np
import psycopg2
from datetime import datetime
from pgvector.psycopg2 import register_vector
from typing import List, Dict, Tuple
from edusystem1.settings import DATABASES
from .image_analyzer_new import VLTextSummarizer, analyze_document

class ErrorRecordManager:

    def __init__(self):
        self.conn = psycopg2.connect(
            dbname="learning_db",
            host="localhost",
            port=5433,
            user="postgres",
            password="123456"
        )
        register_vector(self.conn)
        print("当前API Key:", os.getenv("DASHSCOPE_API_KEY"))
        with self.conn.cursor() as cur:
            cur.execute("SELECT current_database()")
            db_name = cur.fetchone()[0]
            print(f"当前实际连接的数据库: {db_name}")

    def _generate_embeddings(self, texts: List[str]) -> List[np.ndarray]:
        """调用千问API生成向量"""
        try:
            resp = dashscope.TextEmbedding.call(
                model="text-embedding-v4",
                input=texts,
                text_type="document"
            )
            return [np.array(item['embedding']) for item in resp.output['embeddings']]
        except Exception as e:
            print(f"API调用失败: {e}")
            raise

    def save_individual_errors(self, student_id: str, error_data: Dict) -> Tuple[bool, List[Dict]]:
        """
        保存错题到数据库并返回保存的记录
        
        Returns:
            Tuple[bool, List[Dict]]: 
                - bool: 保存是否成功
                - List[Dict]: 保存的记录列表，每个记录包含完整字段信息
        """
        saved_records = []
        
        try:
            print("saving individual errors...")
            print(f"error_data 类型: {type(error_data)}")
            
            with self.conn.cursor() as cursor:
                all_errors = error_data.get("all_data", [])
                questions_to_vectorize = []
                
                # 1. 收集所有需要保存的错题
                for error_group in all_errors:
                    original_input_id = error_group.get("original_input_id", "unknown")
                    wrong_q_list = error_group.get("wrong_q_sum", [])
                    
                    # 过滤有效错题（学生答案≠正确答案）
                    valid_errors = [
                        q for q in wrong_q_list 
                        if q.get("correct_answer") != q.get("student_answer")
                    ]
                    
                    for q in valid_errors:
                        question_id = q.get("question_id", str(hash(q["question"])))
                        unique_id = f"{original_input_id}_{question_id}"
                        questions_to_vectorize.append((unique_id, json.dumps(q)))
                
                print(f"共收集到 {len(questions_to_vectorize)} 个有效错题")
                
                # 2. 批量生成向量
                batch_size = 50
                question_vectors = {}
                for i in range(0, len(questions_to_vectorize), batch_size):
                    batch = questions_to_vectorize[i:i + batch_size]
                    texts = [q[1] for q in batch]
                    vectors = self._generate_embeddings(texts)
                    
                    for (q_id, q_text), vec in zip(batch, vectors):
                        question_vectors[q_id] = vec
                
                # 3. 保存到数据库并收集记录信息
                for unique_id, q_text in questions_to_vectorize:
                    try:
                        cursor.execute("""
                            INSERT INTO study_detail(
                                student_id, original_input_id, details, 
                                details_embedding, created_at
                            ) VALUES (%s, %s, %s, %s, %s)
                            RETURNING study_detail_id, created_at
                        """, (
                            student_id,
                            unique_id.split("_")[0],
                            q_text,
                            json.dumps(question_vectors[unique_id].tolist()),
                            datetime.now()
                        ))
                        
                        # 获取刚插入的记录ID和时间
                        record_id, created_at = cursor.fetchone()
                        
                        # 解析保存的错题详情
                        q_data = json.loads(q_text)
                        
                        # 构建返回的记录信息
                        saved_records.append({
                            'study_detail_id': record_id,
                            'student_id': student_id,
                            'original_input_id': unique_id.split("_")[0],
                            'question': q_data.get('question', ''),
                            'correct_answer': q_data.get('correct_answer', ''),
                            'student_answer': q_data.get('student_answer', ''),
                            'created_at': created_at.strftime('%Y-%m-%d %H:%M:%S'),
                            'details': q_data
                            # 'details_embedding': question_vectors[unique_id].tolist()
                        })
                        # print(f'saved record ID: {saved_records}')
                        
                    except psycopg2.Error as e:
                        print(f"数据库错误: {e}")
                        self.conn.rollback()
                        continue
                
                self.conn.commit()
                print(f"成功保存 {len(saved_records)} 条记录")
                return True, saved_records
                
        except Exception as e:
            print(f"数据库操作失败: {e}")
            self.conn.rollback()
            return False, []

    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()

if __name__ == "__main__":

    image_path = r"D:\vsc\edusystem\src\core\wrongquestion.png"  # 替换为你的图片路径
    print("开始分析图片中的错题信息...")
    error_data = analyze_document(image_path) 
    print("分析结果:", error_data)
    manager = ErrorRecordManager()
    if manager.save_individual_errors(1,error_data):
        print("错题数据存储成功")
    else:
        print("存储失败")