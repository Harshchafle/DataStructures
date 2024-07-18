public class SnakeMartix {

    // Horizontal
    public static void makeSnake(int arr[][]){
        for(int i=0; i<arr.length; i++){
            for(int j=0; j<arr.length; j++){
                if(i%2 == 0){
                    System.out.println(arr[i][j]);
                } else{
                    System.out.println(arr[i][arr.length-j-1]);
                }
            }
        }
    }
    //----------------------------------------------------------------

    //vertical
    public static void makeVertical(int arr[][]) {
        for (int j = 0; j < arr.length; j++  ) {
            for (int i = 0; i < arr.length; i++) {
                if (i % 2 == 0) {
                    System.out.println(arr[i][j]);
                } else {
                    System.out.println(arr[i][arr.length - j - 1]);
                }
            }
        }
    }
    //----------------------------------------------------------------

    /// Transpose
    public static int[][] makeTranspose(int arr[][]){
        for(int i=0; i<arr.length; i++){
            for(int j=i; j<arr.length; j++){
                int temp = arr[i][j];
                arr[i][j] = arr[j][i];
                arr[j][i] = temp;
            }
        }
        return arr;
    }
    //----------------------------------------------------------------

    // printmatrix
    public static void printMatrix(int arr[][]){
        int row = arr.length;
        int col = arr[0].length;
        for(int i=0; i<row; i++){
            for(int j=0; j<col; j++){
                System.out.print(arr[i][j]+" ");
            }System.out.println();
        }
    }
    //----------------------------------------------------------------
    // MAKE SPIRAL MATRIX
    public static int[][] spiralMatrix(int arr[][]){
        int top = 0;
        int btm = arr.length-1;
        int left = 0;
        int right = arr.length-1;

        while(top < btm ){

            // traverse top row (left -> right)
            for(int i=left; i<=right; i++){
                System.out.println(arr[top][i]);
            }
            top++;

            // traversing right (top -> btm)
            for(int i=top; i<=btm; i++){
                System.out.println(arr[i][right]);
            }
            right--;

            // traversing btm row (right -> left)
            for(int i=right; i>=left; i--){
                System.out.println(arr[btm][i]);
            }
            btm--;

            // traverse left (btm -> top)
            for(int i=btm; i<=top; i++){
                System.out.println(arr[i][left]);
            }
            left++;
        }
        return arr;
    }

    // ----------------------------------------------------------------

    // Matrix Multiplication
    public static int[][] multiply(int [][]arr1, int [][]arr2){
        int r1 = arr1.length-1;
        int c1 = arr1[0].length-1;
        int r2 = arr2.length-1;
        int c2 = arr2[0].length-1;
        int mul[][] = new int[r1][r2];

        if(r1 != c2){
            System.out.println("Can't Multiply Matrices");
        } else {
            
            for(int i=0; i<r1; i++){
                for(int j=0; j<c2; j++){
                    for(int k=0; k<r1; k++){
                        mul[i][j] += arr1[i][k]*arr2[k][j];
                    }
                }
            }
        }
        System.out.println("Multiplied Matrix is :");
        printMatrix(mul);
        return mul;
    }

    //----------------------------------------------------------------

    // Method to find target in matrix by binary Search in 2d Array
    // leetcode 240
    public static boolean binarySearch(int arr[][], int target){
        // int row = arr.length;
        // int col = arr[0].length;
        // int left = 0, right = row*col-1;
        
        // while(left <= right){
        //     int mid = left + (right-left)/2;
        //     int midVal = arr[mid/col][mid%col];
            
        //     if(midVal == target){
        //         return true;
        //     }
            
        //     if(midVal > target){
        //         right = mid-1;
        //     } else {
        //         left = mid+1;
        //     }
        // }

        int top = 0; 
        int right = arr[0].length-1;
        while(top >= 0 && top < arr.length && right >= 0 && right < arr[0].length){
            if(target == arr[top][right]){
                System.out.println("top " + top + " right " + right);
                return true;
            } else if(target > arr[top][right]){
                top++;
            } else if(target < arr[top][right]){
                right--;
            }
        }
        return false;
    }

    //----------------------------------------------------------------
    
    // Print Spiral Matrix
    public static void printSpiral(int arr[][]){
        int top = 0;
        int btm = arr.length - 1;
        int left = 0;
        int right = arr.length - 1;

        while(){

            // traverse left col (top -> btm)
            for(int i=top; i>btm; i++){
                System.out.println(arr[i][top]);
            }
            btm--;

            // traverse btm row (left -> right)
            for(int i=left; i>right; i--){
                System.out.println(arr[btm][i]);
            }

            // traverse right col (btm -> top)
            for(int i=btm; i>top; i--){
                System.out.println(arr[btm][i]);
            }

            // traverse top row (rigth -> left)
            for(int i=top; i>btm; i++){
                System.out.println(arr[i][top]);
            }
            btm--;
        }
        
    }

    public static void main(String[] args) {
        int arr[][] = {{1,3,5,9},{2,8,10,11},{4,12,14,15},{6,13,16,19,}};
        // int arr1[][] = { { 1, 2, 3}, { 4, 5, 6}};
        // int arr2[][] = { { 1, 2}, { 4, 5}, { 3, 1}};
        // makeSnake(arr);
        // makeVertical(arr);
        // makeTranspose(arr);
        // printMatrix(arr1);
        // printMatrix(arr2);
        // multiply(arr1, arr2);

        System.out.println(binarySearch(arr, 2));
        
    }
}
