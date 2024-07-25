public class QuickSort {

    // Print method to print array
    static void print(int[] arr){
        for(int i=0; i<arr.length; i++){
            System.out.print(arr[i]);
        }
    }
   
    // Swap method to swap two integers
    static void swap(int[] arr, int i, int j){
        System.out.println("araylength "+arr.length);
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
   
    // Partition method
    static int partition(int[] arr, int start, int end){
        // select pivot element(*Randomly)
        int pivot  = arr[start];
        int count = 0;
        
        //count how much elems are less then pivot
        for(int i=0; i<arr.length; i++){
            if(arr[i] <= pivot) count++;
        }

        //get the pivotindex with help of count
        int pivotIndex = start + count;
        swap(arr, start, pivotIndex);

        //shift left  -> elems less than pivot
        //shift right -> elems greater than pivot
        int i=start, j=end;
        while(i<pivotIndex && j>pivotIndex){
            while(arr[i]<pivot)i++;
            while(arr[j]>pivot)j--;
            if(i<pivotIndex && j>pivotIndex){
                swap(arr, i, j);
                i++;
                j--;
            }
        }
        return pivotIndex;
   }
   
    //QuickSort
    static void quickSort(int arr[], int start, int end){
        if(start >= end) return;
        int pi = partition(arr, start, end);
        quickSort(arr, start, pi-1);
        quickSort(arr, pi +1, end) ;
    }
   
    public static void main(String args[]){ 
        int arr[] = {2,5,3,7,4,8};
        quickSort(arr, 0, arr.length-1);
    }
}

//////////////////////////////////////////////////////////////
/*
public static void quickSort(int nums[], int l, int h){
    if(l>=h){
        return;
    }

    int pivot = partition(nums, l, h);
    quickSort(nums, l, pivotIndex-1);
    quickSort(nums, pivotIndex+1, h);

    public static int partition(int []nums, int l, int h){
        int pivot = nums[l];
        int i = l+1;
        int j=h;

        while(i<=j){
            while(i<=j && nums[i]<=pivot){
                i++;
            }
            while(j>l && nums[j]>pivot){
                j--;
            }

            if(i<j){
                int temp = nums[i];
                nums[i] = nums[j];
                nums[j] = temp;
            }
        }

        int temp = nums[l];
        nums[l] = nums[j];
        nums[j] = temp;

        return j;
    }
}

*/