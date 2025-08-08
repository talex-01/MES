from langAST import (
    Program, Function, Block, VarDecl, Assignment, Print,
    If, While, For, Return, ExprStmt, BinaryOp, UnaryOp,
    FunctionCall, Literal, Variable
)

# valid programs
programa1 = '''
int factorial(int n) {
  if (n <= 1) {
    return 1;
  }
  int r = n * factorial(n - 1);
  return r;
}

int main(int num) {
  int result;
  result = factorial(num);
  print(result);
  return result;
}
'''

programa2 = '''
int main(int n) {
  int fib1 = 0;
  int fib2 = 1;
  int temp;
  int i = 2;

  print(fib1);
  print(fib2);

  for (i = 2; i < n; i++) {
    temp = fib1 + fib2;
    print(temp);
    fib1 = fib2;
    fib2 = temp;
  }
  return fib2;
}
'''

programa3 = '''
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

int main(int number) {
  if (isPrime(number)) {
    print("É primo!");
    return 1;
  } else {
    print("Não é primo!");
    return 0;
  }
  
}
'''
programa4 = '''
int main() {
  bool flag = true;
  bool otherFlag = false;
  int a = 2 + 3 * 4 - 1;
  int b = x + 0;
  int c = 1 * y;
  int d = z * 0;

  if (true) {
    a = 42;
  } else {
    a = 0;
  }

  int e = flag == true;
  int f = otherFlag == false;

  return a + b + c + d + e + f;
}
'''


## Invalid programs

### falta nome da variavel
programa5 = '''   
int main() {
  int = 5;
  return 0;
}
'''

### falta o ponto e virgula
programa6 = '''
int main() {
  int x = 10
  print(x);
  return 0;
}
'''

### falta tipo de retorno na função
programa7 = '''
main() {
  int x = 5;
  return x;
}
'''