
public class ExpPow {
    // Method to calculate power of e = 2.718
    public static double expPow(int n){
        if(n == 0)return 1;
        else return 2.718*expPow(n-1);
    }

    public static void main(String[] args) {
        System.out.println("e^"+n+" : "+expPow(2));
    }
}
