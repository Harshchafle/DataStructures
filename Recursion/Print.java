
public class Print {

    // Method print NUmbers
    public static void printNum(int n){
        System.out.println(n);
        if(n == 0)return;
        printNum(n-1);
    }
    public static void main(String[] args) {
        printNum(10);
    }
}
