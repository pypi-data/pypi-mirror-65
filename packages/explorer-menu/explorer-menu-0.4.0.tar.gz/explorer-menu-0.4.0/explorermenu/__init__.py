

def cmd(command: str, keep_cmd_window: bool = False) -> str:
    keep_flag = '/K' if keep_cmd_window else '/C'
    return f'cmd.exe {keep_flag} {command} || pause'
