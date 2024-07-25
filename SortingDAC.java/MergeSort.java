import java.util.*;
public class MergeSort {
    
   
    public static void merge(int arr[], int l, int mid, int r){
        int i,j,k;
        int n1 = mid-l+1;
        int n2 = r - mid;
        int left[] = new int[n1];
        int right[] = new int[n2];
     
        for(i=0; i<n1; i++)
            left[i] = arr[i+l];
        for(j=0; j<n2; j++) 
            right[j] = arr[mid+1+j];
      
        i=0;j=0;k=l;
   
        while(i<n1 && j<n2){
            if(left[i]<right[j]){
                arr[k++] = left[i++];
            } else{
                arr[k++] = right[j++];
            }
        }
     
        while(i<n1){
            arr[k++] = left[i++];
        }
     
        while(j<n2){
            arr[k++] = right[j++];
        }
    }
   
    static void mergeSort(int arr[], int l,int r){
        int mid = (r+l)/2;
        if(l >= r) return;
        mergeSort(arr, l, mid);
        mergeSort(arr, mid+1, r);
        merge(arr, l, mid, r);
     
    }
   
    static void print(int arr[]){
        for(int i=0; i<arr.length; i++){
            System.out.print(arr[i]+" ");
        }
        System.out.println();
    }
   
    public static void main(String args[]){ 
        int arr[]={1, 4, 8, 5, 7, 3, 10, 34, 11};
        int n= arr.length;
        System.out.println("Original Array : ");
        print(arr);
        mergeSort(arr, 0, n-1);
        System.out.println("Sorted Array : ");
        print(arr);
   
    }
}
