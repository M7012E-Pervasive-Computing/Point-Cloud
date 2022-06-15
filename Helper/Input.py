
class Input():
    
    @staticmethod
    def get_int_input(max: int, print_str: str = '> ') -> int: 
        """Get a user int input which is between 0 and max.

        Args:
            max (int): max value of user input.
            print_str (str, optional): The str printed. Defaults to '> '.

        Returns:
            int: value picked by user.
        """
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