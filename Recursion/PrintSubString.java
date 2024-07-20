package Recursion;

class PrintSubString{
    //method to get SubString
    public static void printSS(String str, String ans){
        if(str.length() == 0){
            System.out.println(ans);
            return;
        }
        char ch = str.charAt(0);
        printSS(str.substring(1), ans);
        printSS(str.substring(1), ans+ch);
    }

    public static void main(String[] args) {
        printSS("abc","" );
    }

}