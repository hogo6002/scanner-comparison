package com.example;

import org.apache.commons.lang3.StringUtils;

/**
 * Hello world!
 *
 */
public class App 
{
    public static void main( String[] args )
    {
        String message = "  Hello, World!  ";
        System.out.println("Original message: '" + message + "'");

        // Use a function from Apache Commons Lang to remove leading and trailing whitespace
        String trimmedMessage = StringUtils.strip(message);
        System.out.println("Trimmed message: '" + trimmedMessage + "'");

        String nullString = null;
        // Use a function to check if a string is null or empty
        boolean isNullOrEmpty = StringUtils.isEmpty(nullString);
        System.out.println("Is nullString null or empty? " + isNullOrEmpty);

        String blankString = "   ";
        // Use a function to check if a string is null, empty, or whitespace
        boolean isBlank = StringUtils.isBlank(blankString);
        System.out.println("Is blankString null, empty, or whitespace? " + isBlank);

        String text = "java is fun";
        // Use a function to capitalize the first letter
        String capitalizedText = StringUtils.capitalize(text);
        System.out.println("Capitalized text: " + capitalizedText);
    }
}
