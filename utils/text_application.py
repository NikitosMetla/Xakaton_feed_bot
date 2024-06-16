def text_application(application_data: dict) -> str:
    return "\n".join([f"<b>{key}</b>: {application_data.get(key).split('|')[0]}"
                      if key not in ["message_id", 'number_question'] else "" for key in application_data.keys()])