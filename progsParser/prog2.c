int main() {
    int n = 10;
    int fib1 = 0;
    int fib2 = 1;
    int temp;
    int i = 0;
    
    print(fib1);
    print(fib2);
    
    for (i = 2; i < n; i++) {
        temp = fib1 + fib2;
        print(temp);
        fib1 = fib2;
        fib2 = temp;
    }
    
    return 0;
}