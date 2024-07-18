import autogen

config_list = autogen.config_list_from_json(
    env_or_file="OAI_CONFIG_LIST.json",
)

llm_config = {
    "cache_seed": 47,
    "temperature": 0,
    "config_list": config_list,
    "timeout": 120,
}

logging_session_id = autogen.runtime_logging.start(config={"dbname": "logs.db"})
print("Logging session ID: " + str(logging_session_id))

executor = autogen.UserProxyAgent(
    name="Executor",
    system_message="""
    Executor. Execute the code given by the user and suggest updates if there are errors. 
    """,
    human_input_mode="NEVER",
    code_execution_config={
        "last_n_messages": 3,
        "work_dir": "code",
        "use_docker": False,
    },
)

coder = autogen.AssistantAgent(
    name="Optimizer",
    llm_config=llm_config,
    system_message="""
    Optimizer. You are a python expert programmer. Your job is to optimize python code. Implement the suggestions for updates from the Executor as well while optimizing code.
    Role:
    1. Analyze code before optimizing.
    2. Follow good coding practices and make sure the code is clean and efficient.
    3. Eliminate redundant code and optimize algorithms.
    4. Use meaningful names and add necessary comments.
    Note:
    Make sure to save the new code to disk.
    Save the code in a file use "optimized.py" while naming, put # filename: optimized.py inside the code block as the first line.
    Say "TERMINATE" if no more optimizations.
    """,
)

group_chat = autogen.GroupChat(
    agents=[executor, coder], messages=[], max_round=15, speaker_selection_method="round_robin"
)

manager = autogen.GroupChatManager(groupchat=group_chat, llm_config=llm_config)

def optimize(file_content):
    executor.initiate_chat(
    manager,
    message= file_content
)
    autogen.runtime_logging.stop()
    return logging_session_id