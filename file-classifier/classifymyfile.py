class classify:
    def __init__(self)-> None:
        pass
    @staticmethod
    def myfile(file_to_be_classified: str):
        path_contents= file_to_be_classified.split('.')
        if len(path_contents)> 1:
            return path_contents[-1]
        else:
            return None
        