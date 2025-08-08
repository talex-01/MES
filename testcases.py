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
int main(int x, int y, int z) {
  bool flag = true;
  bool otherFlag = false;
  int a = (2 + 3) * (4 - 1);
  int b = x + 3;
  int c = 1 * y;
  int d = z * 1;

  if (b > 5) {
    a = a + d;
  } else {
    a = a - d;
  }

  int e = flag == true;
  int f = otherFlag == false;

  int r = a + b + c + d + e + f;
  return r;
}
'''



## Invalid programs
### falat nome da variavel
programa5 = '''   
int main() {
  int = 5;
}
'''

### falta o ponto e virgula e )
programa6 = '''
int main() {
  print(42
}
'''


### falta o nome da variavel que recebe
programa7 = '''
int f(int) {
  return 0;
}
'''


