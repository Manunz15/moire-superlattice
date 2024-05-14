class Printable:
    def __init__(self) -> None:
        self.k: float = 0
        self.k_err: float = 0

    def __str__(self) -> str:
        return rf'k = ({self.k:.3f} ± {self.k_err:.3f})W/Km'
    
    def __format__(self, format_spec: str) -> str:
        if format_spec[0] == '.' and format_spec[-1] == 'f':
            num = format_spec[1: -1]
            try:
                return rf'k = ({self.k:.{int(num)}f} ± {self.k_err:.{int(num)}f})W/Km'
            except:
                raise TypeError(f"'{num}' is not an integer number.")
        else:
            raise TypeError(f"'{format_spec}' does not exist as format spec for this object. Try instead '.nf' with n an integer number.")