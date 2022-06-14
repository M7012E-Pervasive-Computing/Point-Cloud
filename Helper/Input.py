
class Input():
    
    @staticmethod
    def get_int_input(max: int, print_str: str = '') -> int: 
        result = 0
        while True:
            try:
                result = int(input(print_str))
                if result > max or result < 0: 
                    print('Not a valid index')
                    continue
                break
            except ValueError:
                print('Not a valid input')
        return result