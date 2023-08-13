package Dice;

/*
 * @author Tatenda Samudzi
 */
import java.util.*;

public class Dice {
    int Roll(int num) {
        int val = 0;
        Random rand = new Random();
        val = rand.nextInt(num);
        return val;
    }

    public static void main(String[] args) {
        Scanner scnr = new Scanner(System.in);
        Dice dice = new Dice();
        System.out.println("Enter the number of sides you want the dice to have: ");
        int uBound = scnr.nextInt();
        int outCome = dice.Roll(uBound);
        scnr.close();
        System.out.printf("You rolled a %d\n", outCome);
        System.out.printf("Thank you!");
    }
}