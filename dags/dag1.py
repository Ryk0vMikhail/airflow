from datetime import datetime
from airflow.models import DAG
from airflow.operators.bash import BashOperator


defaul_args = {
    "owner": "etl_user",
    "depends_on_past": False,
    "start_date": datetime(2024, 11, 20)
}

dag = DAG('dag1', default_args=defaul_args, schedule_interval='0 1 * * *', catchup=True,
          max_active_tasks=3, max_active_runs=1, tags=["Test", "First"])

task1 = BashOperator(
    task_id='task1',
    bash_command='python3 /airflow/scripts/dag1/task1.py',
    dag=dag)

task2 = BashOperator(
    task_id='task2',
    bash_command='python3 /airflow/scripts/dag1/task2.py',
    dag=dag)

task1 >> task2