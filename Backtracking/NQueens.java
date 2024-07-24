import java.util.*;

/**
 * NQueens
 */
public class NQueens {

    // Method of Backtracking
    public static List<List<String>> solveNQueens(int n) {
        List<List<String>> list = new ArrayList<>();
        boolean [][]mat = new boolean[n][n];

        nQueens(mat, 0, list, n);
        System.out.println(list);
        return list;
    }

    public static void nQueens(boolean mat[][], int row, List<List<String>> list, int n){
        if(row == n){
            addList(mat, list);
        }
    
        for(int col=0; col<n; col++){
            if(isSafe(row, col, mat)){

            }
        }

    }

    public static boolean isSafe(int row, int col, boolean [][]mat){
        for(int i=row-1; i>=0; i--){
            if(mat[i][col]){
                return false;
            }
        }

        for(int i=row-1, j=col-1; i>=0 && j>=0; i--,j--){
            if(mat[i][j]){
                return false;
            }
        }

        for(int i=row-1, j=col+1; i>=0 && j<mat.length; i--,j++){
            if(mat[i][j]){
                return false;
            }
        }

        return true;
    }

    public static void addList(boolean [][]mat, List<List<String>> list){
        List<String> ans = new ArrayList<>();

        for(int i=0; i<mat.length; i++){
            String str = "";

            for(int j=0; j<mat.length; j++){
                if(mat[i][j]){
                    str += "Q";
                } else {
                    str += ".";
                }
            }
            ans.add(str);
        }
        list.add(ans);
    }

    

    public static void main(String[] args) {
        solveNQueens(4);
    }
}