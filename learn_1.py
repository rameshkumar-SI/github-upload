# step 1 - import all dependancies 
from airflow import DAG
from datetime import datetime,timedelta
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

# step 2 define default arguments
default_args = {
    'owner':'airflow',
    'depends_on_past':False,
    'email':['ramesh@airflow.com'],
    'email_on_failure':False,
    'email_on_retry':False,
    'retries':1,
    'retry_delay': timedelta(minutes=5),
    'start_date':datetime(2021,2,1)
    #'queue':'bash_queue',
    #'pool' :''backfill',
    #'priority_weight':10,
    #'end_date':datetime(2022,12,31)
    #'wait_for_downstream': False
    #'dag':dag,
    #'sla'=timedelta(hours=2)
    #'execution_timeout':timedelta(seconds=300),
    #'on_failure_callback':some_function,
    #'on_success_callback':some_function,
    #'on_retry_callback': another_function,
    #'sla_miss_callback': yet_another_function,
    #'trigger_rule':'all_sucess'
}

dag = DAG(
    'learn_1',
    default_args=default_args,
    description='A simple tutorial DAG',
    schedule_interval=timedelta(days=1),
    tags =['learning'],
    catchup=False
    )

t1 = BashOperator(
    task_id = 'print_date',
    bash_command='date',
    dag=dag
)

t2 = BashOperator(
    task_id ='sleep',
    depends_on_past=False,
    bash_command='sleep 5',
    retries =3,
    dag=dag
)
dag.doc_md = __doc__
t1.doc_md = """ \
    #### Task documentation
    Here we can write any information...

    """
templated_command = """
{% for i in range(5) %}
    echo "{{ ds }}"
    echo "{{ macros.ds_add(ds,7)}}"
    echo "{{params.my_param}}"
{% endfor %}
"""
t3 = BashOperator(
    task_id='templated',
    depends_on_past = False,
    bash_command=templated_command,
    params={'my_param':'parameter I passed in'},
    dag = dag
)

t1 >> [t2,t3]