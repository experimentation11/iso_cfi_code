class CFIValidator:
    """
    Validator and generator for ISO 10962 CFI (Classification of Financial Instruments) codes.
    
    The CFI code consists of six alphabetic characters:
    - First character: Category (Mandatory)
    - Second character: Group (Mandatory)
    - Characters 3-6: Attributes (Can be X if not applicable)
    """
    
    # Valid categories
    CATEGORIES = {
        'E': 'Equities',
        'D': 'Debt instruments',
        'R': 'Entitlements (Rights)',
        'O': 'Options',
        'F': 'Futures',
        'S': 'Swaps',
        'H': 'Forward rate agreements and forward foreign exchange',
        'M': 'Others/Miscellaneous',
        'I': 'Spot',
        'J': 'Deposits, Credits and Current accounts',
        'K': 'Loans',
        'L': 'Spot foreign exchange',
        'T': 'Referential instruments'
    }
    
    # Valid groups for each category
    GROUPS = {
        'E': {
            'S': 'Shares', 
            'U': 'Units (e.g., Unit trusts/Mutual funds)', 
            'F': 'Exchange Traded Funds (ETF)', 
            'L': 'Limited partnership units', 
            'H': 'Equity-held investment instruments', 
            'R': 'Real Estate Investment Trusts (REITs)', 
            'P': 'Protected and guaranteed equities', 
            'C': 'Cooperative', 
            'X': 'Other/Miscellaneous equities'
        },
        'D': {
            'B': 'Bonds', 
            'T': 'Treasury notes/bonds', 
            'C': 'Convertible bonds', 
            'Y': 'Money market instruments', 
            'G': 'Structured instruments (with capital guarantee)', 
            'F': 'Bonds with warrants attached', 
            'P': 'Perpetual bonds', 
            'S': 'Structured instruments (without capital guarantee)', 
            'I': 'Inflation linked bonds'
        },
        'R': {
            'S': 'Subscription rights', 
            'D': 'Dividend right certificates', 
            'P': 'Preference', 
            'L': 'Loyalty premiums', 
            'F': 'Founders shares', 
            'Q': 'Preference shares', 
            'W': 'Warrants', 
            'B': 'Redeemable preferred stocks', 
            'T': 'Miscellaneous entitlements'
        },
        'O': {
            'C': 'Call options', 
            'P': 'Put options', 
            'X': 'Options on options', 
            'W': 'Warrants', 
            'F': 'Future options', 
            'S': 'Spread options', 
            'R': 'Basket options', 
            'I': 'Index options', 
            'J': 'Currency options'
        },
        'F': {
            'F': 'Financial futures', 
            'X': 'Options on futures', 
            'I': 'Index futures', 
            'R': 'Interest rate futures', 
            'E': 'Currency futures', 
            'C': 'Commodity futures', 
            'O': 'Other futures', 
            'W': 'Weather-related futures', 
            'B': 'Bond futures'
        },
        'S': {
            'I': 'Interest rate', 
            'F': 'Foreign exchange', 
            'B': 'Basis', 
            'X': 'Exchange swaps and cross-currency swaps', 
            'S': 'Securities', 
            'W': 'Weather-related swaps', 
            'R': 'Return swaps', 
            'K': 'Commodity', 
            'P': 'Options on swaps (swaptions)'
        },
        'H': {
            'F': 'Forward foreign exchange agreements', 
            'I': 'Forward rate agreements', 
            'X': 'Other'
        },
        'M': {
            'C': 'Commodity', 
            'R': 'Reference rate', 
            'O': 'Other', 
            'F': 'Foreign exchange'
        },
        'I': {
            'X': 'Other', 
            'F': 'Foreign exchange', 
            'C': 'Commodity', 
            'E': 'Equity', 
            'S': 'Securities', 
            'O': 'Options'
        },
        'J': {
            'D': 'Deposits', 
            'C': 'Credits', 
            'N': 'Non-redeemable money market instruments', 
            'R': 'Redeemable money market instruments', 
            'S': 'Structured capital guarantee'
        },
        'K': {
            'L': 'Leveraged', 
            'C': 'Consumer', 
            'M': 'Mortgage', 
            'S': 'Syndicated', 
            'G': 'Government', 
            'P': 'Private', 
            'F': 'Federal agency', 
            'A': 'Agriculture'
        },
        'L': {
            'S': 'Spot'
        },
        'T': {
            'I': 'Interest/Yield rates', 
            'R': 'Reference rates', 
            'F': 'Foreign exchange rates', 
            'U': 'Economic indicators', 
            'V': 'Inflation rates', 
            'N': 'Reference indexes'
        }
    }
    
    # Valid attribute combinations for positions 3-6 based on category-group
    ATTRIBUTES = {
        # Equities
        'ES': {  # Shares
            3: {
                'V': 'Voting', 
                'N': 'Non-voting', 
                'R': 'Restricted voting', 
                'X': 'Not applicable/Not specified'
            },
            4: {
                'R': 'Restricted', 
                'N': 'Free', 
                'X': 'Not applicable/Not specified'
            },
            5: {
                'P': 'Partly paid', 
                'F': 'Fully paid', 
                'X': 'Not applicable/Not specified'
            },
            6: {
                'B': 'Bearer', 
                'R': 'Registered', 
                'X': 'Not applicable/Not specified'
            }
        },
        'EU': {  # Units
            3: {
                'O': 'Open-end', 
                'C': 'Closed-end', 
                'X': 'Not applicable/Not specified'
            },
            4: {
                'R': 'Restricted', 
                'N': 'Free', 
                'X': 'Not applicable/Not specified'
            },
            5: {
                'D': 'Limited dividend', 
                'C': 'Cumulative', 
                'X': 'Not applicable/Not specified'
            },
            6: {
                'B': 'Bearer', 
                'R': 'Registered', 
                'X': 'Not applicable/Not specified'
            }
        },
        'EF': {  # ETF
            3: {
                'O': 'Open-end', 
                'C': 'Closed-end', 
                'X': 'Not applicable/Not specified'
            },
            4: {
                'R': 'Restricted', 
                'N': 'Free', 
                'X': 'Not applicable/Not specified'
            },
            5: {
                'S': 'Synthetic', 
                'P': 'Physical', 
                'H': 'Hybrid', 
                'X': 'Not applicable/Not specified'
            },
            6: {
                'B': 'Bearer', 
                'R': 'Registered', 
                'X': 'Not applicable/Not specified'
            }
        },
        
        # Debt instruments
        'DB': {  # Bonds
            3: {
                'F': 'Fixed rate', 
                'Z': 'Zero coupon', 
                'V': 'Variable rate', 
                'I': 'Inflation linked', 
                'X': 'Not applicable/Not specified'
            },
            4: {
                'S': 'Secured/Collateralized', 
                'U': 'Unsecured/Uncollateralized', 
                'X': 'Not applicable/Not specified'
            },
            5: {
                'G': 'Government/State guarantee', 
                'S': 'Supranational guarantee', 
                'C': 'Corporate guarantee', 
                'X': 'Not applicable/Not specified'
            },
            6: {
                'B': 'Bearer', 
                'R': 'Registered', 
                'X': 'Not applicable/Not specified'
            }
        },
        'DT': {  # Treasury notes/bonds
            3: {
                'F': 'Fixed rate', 
                'Z': 'Zero coupon', 
                'V': 'Variable rate', 
                'I': 'Inflation linked', 
                'X': 'Not applicable/Not specified'
            },
            4: {
                'S': 'Secured/Collateralized', 
                'U': 'Unsecured/Uncollateralized', 
                'X': 'Not applicable/Not specified'
            },
            5: {
                'G': 'Government/State guarantee', 
                'S': 'Supranational guarantee', 
                'X': 'Not applicable/Not specified'
            },
            6: {
                'B': 'Bearer', 
                'R': 'Registered', 
                'X': 'Not applicable/Not specified'
            }
        },
        
        # Options
        'OC': {  # Call options
            3: {
                'A': 'American', 
                'B': 'Bermuda', 
                'E': 'European', 
                'X': 'Not applicable/Not specified'
            },
            4: {
                'S': 'Standard', 
                'N': 'Non-standard', 
                'X': 'Not applicable/Not specified'
            },
            5: {
                'P': 'Physical', 
                'C': 'Cash', 
                'X': 'Not applicable/Not specified'
            },
            6: {
                'X': 'Not applicable/Not specified'
            }
        },
        'OP': {  # Put options
            3: {
                'A': 'American', 
                'B': 'Bermuda', 
                'E': 'European', 
                'X': 'Not applicable/Not specified'
            },
            4: {
                'S': 'Standard', 
                'N': 'Non-standard', 
                'X': 'Not applicable/Not specified'
            },
            5: {
                'P': 'Physical', 
                'C': 'Cash', 
                'X': 'Not applicable/Not specified'
            },
            6: {
                'X': 'Not applicable/Not specified'
            }
        },
        
        # Futures
        'FF': {  # Financial futures
            3: {
                'X': 'Not applicable/Not specified'
            },
            4: {
                'S': 'Standard', 
                'N': 'Non-standard', 
                'X': 'Not applicable/Not specified'
            },
            5: {
                'P': 'Physical', 
                'C': 'Cash', 
                'X': 'Not applicable/Not specified'
            },
            6: {
                'X': 'Not applicable/Not specified'
            }
        },
        
        # Swaps
        'SI': {  # Interest rate
            3: {
                'F': 'Fixed-floating', 
                'L': 'Fixed-fixed', 
                'V': 'Floating-floating', 
                'X': 'Not applicable/Not specified'
            },
            4: {
                'S': 'Single currency', 
                'M': 'Multi-currency', 
                'X': 'Not applicable/Not specified'
            },
            5: {
                'X': 'Not applicable/Not specified'
            },
            6: {
                'X': 'Not applicable/Not specified'
            }
        }
        
        # Additional category-group combinations would be defined similarly
    }
    
    @staticmethod
    def validate(cfi_code):
        """
        Validates a CFI code according to ISO 10962 standard.
        
        Args:
            cfi_code (str): The 6-character CFI code to validate
            
        Returns:
            tuple: (bool, str) - (is_valid, error_message)
        """
        # Basic validation
        if not cfi_code or not isinstance(cfi_code, str):
            return False, "CFI code must be a string"
            
        if len(cfi_code) != 6:
            return False, "CFI code must be exactly 6 characters"
            
        if not cfi_code.isalpha():
            return False, "CFI code must contain only alphabetic characters"
            
        cfi_code = cfi_code.upper()
        
        # Validate first character (Category)
        category = cfi_code[0]
        if category not in CFIValidator.CATEGORIES:
            return False, f"Invalid category '{category}'. Must be one of: {', '.join(CFIValidator.CATEGORIES.keys())}"
        
        # Validate second character (Group) based on the category
        group = cfi_code[1]
        if group not in CFIValidator.GROUPS.get(category, {}):
            return False, f"Invalid group '{group}' for category '{category}'. Valid groups: {', '.join(CFIValidator.GROUPS[category].keys())}"
        
        # Validate characters 3-6 based on the category-group combination
        category_group = category + group
        
        # If we have specific attribute validations for this category-group
        if category_group in CFIValidator.ATTRIBUTES:
            for position in range(2, 6):  # Positions 2-5 (0-indexed) correspond to characters 3-6
                char = cfi_code[position]
                position_index = position + 1  # Convert to 1-indexed for error messages
                
                # Check if we have validation rules for this position
                if position + 1 in CFIValidator.ATTRIBUTES[category_group]:
                    valid_chars = CFIValidator.ATTRIBUTES[category_group][position + 1].keys()
                    if char not in valid_chars:
                        return False, f"Invalid attribute '{char}' at position {position_index} for {category_group}. Valid options: {', '.join(valid_chars)}"
                else:
                    # If no specific rules, at least ensure it's alphabetic or X
                    if not char.isalpha():
                        return False, f"Character at position {position_index} must be alphabetic"
        else:
            # For category-group combinations without specific rules,
            # just ensure characters 3-6 are alphabetic or X
            for i in range(2, 6):
                if not (cfi_code[i].isalpha()):
                    position_index = i + 1
                    return False, f"Character at position {position_index} must be alphabetic"
        
        return True, f"Valid CFI code for {CFIValidator.CATEGORIES[category]} - {CFIValidator.GROUPS[category][group]}"
    
    @staticmethod
    def format_attribute_options(category, group, position):
        """
        Returns formatted options for a specific attribute position.
        
        Args:
            category (str): Category character
            group (str): Group character
            position (int): Position (3-6)
            
        Returns:
            str: Formatted options for display
        """
        category_group = category + group
        if category_group in CFIValidator.ATTRIBUTES and position in CFIValidator.ATTRIBUTES[category_group]:
            options = CFIValidator.ATTRIBUTES[category_group][position]
            return "\n".join([f"  {key} - {value}" for key, value in options.items()])
        else:
            return "  X - Not applicable/Not specified"
    
    @staticmethod
    def generate_cfi_code():
        """
        Interactive function to help user generate a valid CFI code.
        
        Returns:
            str: Generated CFI code
        """
        print("\nCFI Code Generator")
        print("=================")
        
        # Step 1: Select Category
        print("\nStep 1: Select Category (First Character)")
        for key, value in CFIValidator.CATEGORIES.items():
            print(f"  {key} - {value}")
        
        while True:
            category = input("\nEnter category code: ").upper()
            if category in CFIValidator.CATEGORIES:
                print(f"Selected: {category} - {CFIValidator.CATEGORIES[category]}")
                break
            else:
                print(f"Invalid category. Please select from: {', '.join(CFIValidator.CATEGORIES.keys())}")
        
        # Step 2: Select Group
        print("\nStep 2: Select Group (Second Character)")
        for key, value in CFIValidator.GROUPS[category].items():
            print(f"  {key} - {value}")
        
        while True:
            group = input("\nEnter group code: ").upper()
            if group in CFIValidator.GROUPS[category]:
                print(f"Selected: {group} - {CFIValidator.GROUPS[category][group]}")
                break
            else:
                print(f"Invalid group. Please select from: {', '.join(CFIValidator.GROUPS[category].keys())}")
        
        category_group = category + group
        cfi_code = category + group
        
        # Step 3-6: Select Attributes
        for position in range(3, 7):
            print(f"\nStep {position}: Select Attribute (Character {position})")
            
            if category_group in CFIValidator.ATTRIBUTES and position in CFIValidator.ATTRIBUTES[category_group]:
                print(CFIValidator.format_attribute_options(category, group, position))
                
                while True:
                    attr = input(f"\nEnter attribute {position} code: ").upper()
                    if attr in CFIValidator.ATTRIBUTES[category_group][position] or attr == 'X':
                        if attr in CFIValidator.ATTRIBUTES[category_group][position]:
                            print(f"Selected: {attr} - {CFIValidator.ATTRIBUTES[category_group][position][attr]}")
                        else:
                            print("Selected: X - Not applicable/Not specified")
                        cfi_code += attr
                        break
                    else:
                        valid_options = list(CFIValidator.ATTRIBUTES[category_group][position].keys())
                        if 'X' not in valid_options:
                            valid_options.append('X')
                        print(f"Invalid attribute. Please select from: {', '.join(valid_options)}")
            else:
                print("No specific attributes defined for this position.")
                print("  X - Not applicable/Not specified is recommended")
                attr = input(f"\nEnter attribute {position} code (or press Enter for 'X'): ").upper()
                if not attr:
                    attr = 'X'
                cfi_code += attr
        
        # Validate the final code (should be valid, but just to be sure)
        is_valid, message = CFIValidator.validate(cfi_code)
        if is_valid:
            print(f"\nGenerated valid CFI code: {cfi_code}")
            return cfi_code
        else:
            print(f"\nWarning: Generated code {cfi_code} is not valid: {message}")
            print("Please try generation again.")
            return None


def display_cfi_details(cfi_code):
    """
    Display detailed information about a valid CFI code.
    
    Args:
        cfi_code (str): The validated CFI code
    """
    cfi_code = cfi_code.upper()
    category = cfi_code[0]
    group = cfi_code[1]
    category_group = category + group
    
    print(f"\nCFI Code: {cfi_code}")
    print("======================")
    print(f"Category (1st): {category} - {CFIValidator.CATEGORIES.get(category, 'Unknown')}")
    print(f"Group (2nd): {group} - {CFIValidator.GROUPS.get(category, {}).get(group, 'Unknown')}")
    
    # Display attributes if we have details
    if category_group in CFIValidator.ATTRIBUTES:
        for pos in range(2, 6):
            char = cfi_code[pos]
            pos_index = pos + 1
            
            if pos_index in CFIValidator.ATTRIBUTES[category_group] and char in CFIValidator.ATTRIBUTES[category_group][pos_index]:
                attr_desc = CFIValidator.ATTRIBUTES[category_group][pos_index][char]
                print(f"Attribute {pos_index}: {char} - {attr_desc}")
            else:
                if char == 'X':
                    print(f"Attribute {pos_index}: {char} - Not applicable/Not specified")
                else:
                    print(f"Attribute {pos_index}: {char}")
    else:
        for pos in range(2, 6):
            char = cfi_code[pos]
            pos_index = pos + 1
            if char == 'X':
                print(f"Attribute {pos_index}: {char} - Not applicable/Not specified")
            else:
                print(f"Attribute {pos_index}: {char}")


def main():
    """
    Main function to run the CFI code validator and generator application.
    """
    print("ISO 10962 CFI Code Validator and Generator")
    print("========================================")
    
    while True:
        print("\nOptions:")
        print("1. Validate a CFI code")
        print("2. Generate a CFI code")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ")
        
        if choice == '1':
            # Validate CFI code
            cfi_code = input("\nEnter CFI code to validate: ")
            is_valid, message = CFIValidator.validate(cfi_code)
            
            if is_valid:
                print(f"\n✓ {message}")
                display_cfi_details(cfi_code)
            else:
                print(f"\n✗ {message}")
        
        elif choice == '2':
            # Generate CFI code
            generated_code = CFIValidator.generate_cfi_code()
            if generated_code:
                print("\nGenerated CFI code details:")
                display_cfi_details(generated_code)
        
        elif choice == '3':
            print("\nExiting program. Goodbye!")
            break
        
        else:
            print("\nInvalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
