import java.util.List;

/**
 * WordSearch
 */
public class WordSearch {
    public static boolean exist(char board[][], String word){
        int m = board.length;
        int n = board[0].length;
        boolean visited[][] = new boolean[m][n];

        for(int i=0; i<board.length; i++){
            for(int j=0; j<board[0].length; j++){
                if(board[i][j] == word.charAt(0)){
                    if(wordSearch(board, visited, word, 0, i, j)){
                        return true;
                    }
                }
            }
        }
        return false;

    }

    public static boolean wordSearch(char[][]board, boolean[][] visited, String word, int ind, int i, int j){
        if(ind == word.length()){
            return true;
        }
        if(i<0 || i == board.length || j<0 || j== board[0].length || visited[i][j] || board[i][j] != word.charAt(ind)){
            return false;
        }
        visited[i][j] = true;
        if(wordSearch(board, visited, word, ind+1, i-1, j)){
            return true;
        }
        return false;
    }
    public static void main(String[] args) {
        char [][]ch = {
                        {'a','d','f'},
                        {'h','a','h'},
                        {'c','r','s'}
                      };
        System.out.println(exist(ch, "harsh"));
    }

}
