import java.util.Scanner;

public class Node<T> {
    T data;
    Node next;

    public Node(){}

    public Node(T data){
        this.data = data;
    }


    public static void main(String[] args) {
        Node <Integer> n1 = new Node<>(2);
        Node<String> n2 = new Node<>("Harsh");
        n1.next = n2;
        System.out.println(n1);
        System.out.println(n2);
        System.out.println(n1.data+" -> "+n1.next.data);

        // 
        Scanner sc = new Scanner(System.in);
        System.out.println("Enter number of node in a list : ");
        int num = sc.nextInt();
        Node<Integer> head = null;
        Node<Integer> tail = null;
        for(int i=0; i<num; i++){
            Node<Integer> n = new Node<>(sc.nextInt());
            if(head == null){
                head = n;
                tail = n;
            } else {
                tail.next = n;
                tail = n;
            }
        }
        Node<Integer> temp = head;
        while(temp != null){
            System.out.print(temp.data+" -> ");
            temp = temp.next;
        }System.out.println("NULL");

    }
}