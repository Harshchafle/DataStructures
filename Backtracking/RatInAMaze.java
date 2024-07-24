//{ Driver Code Starts
// Initial Template for Java

import java.util.*;

class Rat {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int t = sc.nextInt();

        while (t-- > 0) {
            int n = sc.nextInt();
            int[][] a = new int[n][n];
            for (int i = 0; i < n; i++)
                for (int j = 0; j < n; j++) a[i][j] = sc.nextInt();

            Solution obj = new Solution();
            ArrayList<String> res = obj.findPath(a);
            Collections.sort(res);
            if (res.size() > 0) {
                for (int i = 0; i < res.size(); i++) System.out.print(res.get(i) + " ");
                System.out.println();
            } else {
                System.out.println(-1);
            }
        }
    }
}

// } Driver Code Ends


// User function Template for Java

// m is the given matrix and n is the order of matrix
class Solution {
    public ArrayList<String> findPath(int[][] mat) {
        // Your code here
        ArrayList<String> list = new ArrayList<String>();
        boolean[][] visited = new boolean[mat.length][mat.length];
        ratInAMaze(mat, 0, 0, visited, "", list);
        return list;
        
    }
    
    public static void ratInAMaze(int[][]mat, int i, int j, boolean[][] visited, String psf,List<String> list ){
        if(i == mat.length-1 && j == mat.length-1 && mat[i][j] == 1){
            list.add(psf);
            return;
        }
        
        if(i<0 || i==mat.length || j<0 || j==mat.length || mat[i][j] == 0 || visited[i][j]){
            return;
        }
        
        visited[i][j] = true;
        
        ratInAMaze(mat, i-1, j, visited, psf+"U", list);
        ratInAMaze(mat, i, j+1, visited, psf+"R", list);
        ratInAMaze(mat, i+1, j, visited, psf+"D", list);
        ratInAMaze(mat, i, j-1, visited, psf+"L", list);

        visited[i][j] = false;
    }
}