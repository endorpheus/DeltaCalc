#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <ctype.h>

#define MAX_INPUT 100

// Function prototypes
void print_help(void);
double parse_number(char *str, int *valid);
void calculate_delta(double val1, double val2);
void clear_input_buffer(void);

int main(int argc, char *argv[]) {
    double val1, val2;
    char input[MAX_INPUT];
    int valid = 0;

    // Handle command line arguments
    if (argc > 1) {
        if (strcmp(argv[1], "-h") == 0 || strcmp(argv[1], "--help") == 0) {
            print_help();
            return 0;
        }
        
        if (argc == 3) {
            val1 = parse_number(argv[1], &valid);
            if (!valid) {
                fprintf(stderr, "Error: Invalid first number\n");
                return 1;
            }
            
            val2 = parse_number(argv[2], &valid);
            if (!valid) {
                fprintf(stderr, "Error: Invalid second number\n");
                return 1;
            }
            
            calculate_delta(val1, val2);
            return 0;
        }
        
        fprintf(stderr, "Error: Invalid number of arguments\n");
        print_help();
        return 1;
    }

    // Interactive mode
    printf("Δ%% Calculator - Enter 'q' to quit, 'h' for help\n");
    
    while (1) {
        printf("\nFirst value: ");
        if (fgets(input, MAX_INPUT, stdin) == NULL) break;
        
        // Check for quit or help commands
        if (input[0] == 'q' || input[0] == 'Q') break;
        if (input[0] == 'h' || input[0] == 'H') {
            print_help();
            continue;
        }

        val1 = parse_number(input, &valid);
        if (!valid) {
            printf("Error: Please enter a valid number\n");
            clear_input_buffer();
            continue;
        }

        printf("Second value: ");
        if (fgets(input, MAX_INPUT, stdin) == NULL) break;
        
        val2 = parse_number(input, &valid);
        if (!valid) {
            printf("Error: Please enter a valid number\n");
            clear_input_buffer();
            continue;
        }

        calculate_delta(val1, val2);
    }

    printf("\nGoodbye!\n");
    return 0;
}

void print_help(void) {
    printf("\nΔ%% Calculator Usage:\n");
    printf("  Interactive mode: Just run the program\n");
    printf("  Command line mode: delta_calc <value1> <value2>\n");
    printf("\nCommands (interactive mode):\n");
    printf("  h or H - Show this help\n");
    printf("  q or Q - Quit the program\n");
    printf("\nFormula: Δ%% = (1 - smaller/larger) × 100\n");
    printf("Example: 3.58 vs 4.23 → Δ%% = (1 - 3.58/4.23) × 100 = 15.37%%\n");
}

double parse_number(char *str, int *valid) {
    char *endptr;
    double result;
    
    // Skip whitespace
    while (isspace((unsigned char)*str)) str++;
    
    if (*str == '\0') {
        *valid = 0;
        return 0;
    }

    result = strtod(str, &endptr);
    
    // Check if conversion was successful
    if (endptr == str || (*endptr != '\0' && !isspace((unsigned char)*endptr))) {
        *valid = 0;
        return 0;
    }

    *valid = 1;
    return result;
}

void calculate_delta(double val1, double val2) {
    double larger, smaller, delta_percent;
    
    // Handle special cases
    if (val1 == 0 && val2 == 0) {
        printf("Both values are zero\n");
        return;
    }
    
    // Determine which value is larger
    if (fabs(val1) > fabs(val2)) {
        larger = fabs(val1);
        smaller = fabs(val2);
    } else {
        larger = fabs(val2);
        smaller = fabs(val1);
    }

    // Calculate percentage difference
    delta_percent = (1 - smaller/larger) * 100;

    // Print results
    printf("\nLarger value: %.4f\n", larger);
    printf("Smaller value: %.4f\n", smaller);
    printf("Δ%% = %.2f%%\n", delta_percent);
    printf("The smaller value is %.2f%% of the larger value\n", 100 - delta_percent);
    printf("\nFormula: Δ%% = (1 - %.4f/%.4f) × 100\n", smaller, larger);
}

void clear_input_buffer(void) {
    int c;
    while ((c = getchar()) != '\n' && c != EOF);
}
