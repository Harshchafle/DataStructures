package Recursion;

public class FiboNum {
    // Method to get nth finonacci number
    public static int fiboNum(int n){
        if(n == 0 || n == 1) return 0;
        if(n == 2) return 1;
        else return fiboNum(n-1)+fiboNum(n-2);
    }
    public static void main(String[] args) {
        System.out.println(fiboNum(50));
    }
}
