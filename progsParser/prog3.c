int isPrime(int num) {
    if (num <= 1) {
        return 0;  
    }
    if (num <= 3) {
        return 1;  
    }
    if (num % 2 == 0) {
        return 0;  
    }
    
    int i = 3;
    while (i * i <= num) {
        if (num % i == 0) {
            return 0;  
        }
        i = i + 2;
    }
    
    return 1;  
}

int main() {
    int number = 17;
    if (isPrime(number)) {
        print("É primo!");
    } else {
        print("Não é primo!");
    }
    return 0;
}