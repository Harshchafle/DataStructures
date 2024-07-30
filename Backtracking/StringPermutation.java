public class StringPermutation {
    // Method to find Permutations of a String
    public static void printPermutation(String inStr, String permStr, int idx){
        
        if(inStr.length() == 0){
            System.out.println(permStr);
            return;
        }
        
        for(int i=0; i<inStr.length(); i++){
            char currChar = inStr.charAt(i);
            String newStr = inStr.substring(0,i)+inStr.substring(i+1);
            printPermutation(newStr, permStr+currChar, idx);
        }
    }

    // Main Method
    public static void main(String[] args) {
        printPermutation("ABC", "", 0);
    }
}
