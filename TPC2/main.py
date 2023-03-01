def getNums(s : str) -> list:
    nums = []
    aux = []
    for i in range(len(s)):
        if s[i].isdigit():
            aux.append(s[i])
        else:
            if len(aux) > 0:
                nums.append(int(''.join(aux)))
            aux = []
    if len(aux) > 0: # add the last number
        nums.append(int(''.join(aux)))
    return nums

def main() -> None:
    res = 0
    reading = True
    
    while True:
        s = input()
        reading = False if "off" in s.lower() else reading
        reading = True if "on" in s.lower() else reading
        nums = getNums(s)
        if reading:
            res += sum(nums)
        if "=" in s.lower():
            print(res)
    
if __name__ == '__main__':
    main()
