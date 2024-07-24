import java.util.*;

public class GenerateParantheses {
    // Method to generate GenerateParantheses
    public static void generateParantheses(int n, int open, int close, String ans, List<String> list){
        
        if(close == n){
            list.add(ans);
            return;
        }  

        if(open < n){
            generateParantheses(n, open+1, close, ans+"(", list);
        }
        if(close < n  && close < open){
            generateParantheses(n, open, close+1, ans+")", list);
        }
    }

    public static void main(String[] args) {
        int n=4;
        List<String> list = new ArrayList<>();
        generateParantheses(n, 0, 0, "", list);
        System.out.println(list);
    }
}
