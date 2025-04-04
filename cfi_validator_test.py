class CFIValidator:
    """
    Enhanced validator and generator for ISO 10962 CFI (Classification of Financial Instruments) codes.
    
    The CFI code consists of six alphabetic characters:
    - First character: Category (Mandatory)
    - Second character: Group (Mandatory)
    - Characters 3-6: Attributes (Can be X if not applicable)
    """
    
    # Position descriptions for explaining the 6-character structure
    POSITION_DESCRIPTIONS = {
        1: "Category - Primary classification of the financial instrument",
        2: "Group - Secondary classification within the category",
        3: "Attribute 1 - Specific characteristics related to the instrument type",
        4: "Attribute 2 - Additional characteristics/features",
        5: "Attribute 3 - Further specification of the instrument",
        6: "Attribute 4 - Final specification details"
    }
    
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
        Validates a CFI code according to ISO 10962 standard with enhanced position information.
        
        Args:
            cfi_code (str): The 6-character CFI code to validate
            
        Returns:
            tuple: (bool, str, dict) - (is_valid, error_message, positions_info)
        """
        # Prepare positions info dictionary
        positions_info = {}
        for i in range(1, 7):
            positions_info[i] = {
                'description': CFIValidator.POSITION_DESCRIPTIONS[i],
                'value': None,
                'meaning': None,
                'valid': None
            }
        
        # Basic validation
        if not cfi_code or not isinstance(cfi_code, str):
            return False, "CFI code must be a string", positions_info
            
        if len(cfi_code) != 6:
            return False, "CFI code must be exactly 6 characters", positions_info
            
        if not cfi_code.isalpha():
            return False, "CFI code must contain only alphabetic characters", positions_info
            
        cfi_code = cfi_code.upper()
        
        # Validate first character (Category) - Position 1
        category = cfi_code[0]
        positions_info[1]['value'] = category
        
        if category in CFIValidator.CATEGORIES:
            positions_info[1]['meaning'] = CFIValidator.CATEGORIES[category]
            positions_info[1]['valid'] = True
        else:
            positions_info[1]['valid'] = False
            positions_info[1]['error'] = f"Invalid category '{category}'. Must be one of: {', '.join(CFIValidator.CATEGORIES.keys())}"
            return False, positions_info[1]['error'], positions_info
        
        # Validate second character (Group) based on the category - Position 2
        group = cfi_code[1]
        positions_info[2]['value'] = group
        
        if group in CFIValidator.GROUPS.get(category, {}):
            positions_info[2]['meaning'] = CFIValidator.GROUPS[category][group]
            positions_info[2]['valid'] = True
        else:
            positions_info[2]['valid'] = False
            positions_info[2]['error'] = f"Invalid group '{group}' for category '{category}'. Valid groups: {', '.join(CFIValidator.GROUPS[category].keys())}"
            return False, positions_info[2]['error'], positions_info
        
        # Validate characters 3-6 based on the category-group combination
        category_group = category + group
        
        # If we have specific attribute validations for this category-group
        if category_group in CFIValidator.ATTRIBUTES:
            for position in range(2, 6):  # Positions 2-5 (0-indexed) correspond to characters 3-6
                char = cfi_code[position]
                position_index = position + 1  # Convert to 1-indexed for display
                
                positions_info[position_index]['value'] = char
                
                # Check if we have validation rules for this position
                if position_index in CFIValidator.ATTRIBUTES[category_group]:
                    valid_chars = CFIValidator.ATTRIBUTES[category_group][position_index].keys()
                    
                    if char in valid_chars:
                        positions_info[position_index]['meaning'] = CFIValidator.ATTRIBUTES[category_group][position_index][char]
                        positions_info[position_index]['valid'] = True
                    else:
                        positions_info[position_index]['valid'] = False
                        positions_info[position_index]['error'] = f"Invalid attribute '{char}' at position {position_index} for {category_group}. Valid options: {', '.join(valid_chars)}"
                        return False, positions_info[position_index]['error'], positions_info
                else:
                    # If no specific rules, at least ensure it's alphabetic
                    if char.isalpha():
                        positions_info[position_index]['meaning'] = "Custom attribute (no predefined meaning)"
                        positions_info[position_index]['valid'] = True
                    else:
                        positions_info[position_index]['valid'] = False
                        positions_info[position_index]['error'] = f"Character at position {position_index} must be alphabetic"
                        return False, positions_info[position_index]['error'], positions_info
        else:
            # For category-group combinations without specific rules,
            # just ensure characters 3-6 are alphabetic
            for i in range(2, 6):
                position_index = i + 1
                char = cfi_code[i]
                positions_info[position_index]['value'] = char
                
                if char.isalpha():
                    if char == 'X':
                        positions_info[position_index]['meaning'] = "Not applicable/Not specified"
                    else:
                        positions_info[position_index]['meaning'] = "Custom attribute (no predefined meaning)"
                    positions_info[position_index]['valid'] = True
                else:
                    positions_info[position_index]['valid'] = False
                    positions_info[position_index]['error'] = f"Character at position {position_index} must be alphabetic"
                    return False, positions_info[position_index]['error'], positions_info
        
        return True, f"Valid CFI code for {CFIValidator.CATEGORIES[category]} - {CFIValidator.GROUPS[category][group]}", positions_info
    
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
    def get_position_options(category, group, position):
        """
        Returns all valid options for a specific position.
        
        Args:
            category (str): Category character (or None)
            group (str): Group character (or None)
            position (int): Position (1-6)
            
        Returns:
            dict: Valid options and their descriptions
        """
        # Position 1: Categories
        if position == 1:
            return CFIValidator.CATEGORIES
        
        # Position 2: Groups (requires category)
        if position == 2 and category in CFIValidator.CATEGORIES:
            return CFIValidator.GROUPS.get(category, {})
        
        # Positions 3-6: Attributes (requires category and group)
        if position in [3, 4, 5, 6] and category and group:
            category_group = category + group
            if category_group in CFIValidator.ATTRIBUTES and position in CFIValidator.ATTRIBUTES[category_group]:
                return CFIValidator.ATTRIBUTES[category_group][position]
            else:
                return {'X': 'Not applicable/Not specified'}
                
        return {}
    
    @staticmethod
    def generate_cfi_code(initial_prefix=""):
        """
        Interactive function to help user generate a valid CFI code.
        User can provide an initial prefix of at least one character.
        
        Args:
            initial_prefix (str): Optional initial characters of the CFI code
            
        Returns:
            str: Generated CFI code
        """
        print("\nCFI Code Generator")
        print("=================")
        
        # Convert initial prefix to uppercase and validate
        initial_prefix = initial_prefix.upper() if initial_prefix else ""
        
        # Parse the initial prefix to pre-select options
        cfi_code = ""
        category = None
        group = None
        
        if len(initial_prefix) >= 1:
            if initial_prefix[0] in CFIValidator.CATEGORIES:
                category = initial_prefix[0]
                cfi_code += category
                print(f"\nUsing provided category: {category} - {CFIValidator.CATEGORIES[category]}")
            else:
                print(f"Warning: Invalid category '{initial_prefix[0]}' in prefix. Starting from scratch.")
                initial_prefix = ""
        
        if len(initial_prefix) >= 2 and category:
            if initial_prefix[1] in CFIValidator.GROUPS.get(category, {}):
                group = initial_prefix[1]
                cfi_code += group
                print(f"Using provided group: {group} - {CFIValidator.GROUPS[category][group]}")
            else:
                print(f"Warning: Invalid group '{initial_prefix[1]}' for category '{category}'. Keeping only the category.")
                initial_prefix = initial_prefix[0]
        
        # Continue with the remaining characters if valid
        valid_prefix = True
        if len(initial_prefix) > 2 and category and group:
            category_group = category + group
            for i in range(2, min(6, len(initial_prefix))):
                char = initial_prefix[i]
                position = i + 1
                
                if category_group in CFIValidator.ATTRIBUTES and position in CFIValidator.ATTRIBUTES[category_group]:
                    if char in CFIValidator.ATTRIBUTES[category_group][position] or char == 'X':
                        cfi_code += char
                        print(f"Using provided attribute {position}: {char}")
                    else:
                        print(f"Warning: Invalid attribute '{char}' at position {position} for {category_group}. Ignoring the rest of the prefix.")
                        valid_prefix = False
                        break
                else:
                    # If no specific validation, just ensure it's alphabetic
                    if char.isalpha():
                        cfi_code += char
                        print(f"Using provided attribute {position}: {char}")
                    else:
                        print(f"Warning: Non-alphabetic character '{char}' at position {position}. Ignoring the rest of the prefix.")
                        valid_prefix = False
                        break
        
        # Step 1: Select Category (if not provided)
        if not category:
            print("\nStep 1: Select Category (First Character)")
            print(f"Description: {CFIValidator.POSITION_DESCRIPTIONS[1]}")
            for key, value in CFIValidator.CATEGORIES.items():
                print(f"  {key} - {value}")
            
            while True:
                category = input("\nEnter category code: ").upper()
                if category in CFIValidator.CATEGORIES:
                    print(f"Selected: {category} - {CFIValidator.CATEGORIES[category]}")
                    cfi_code += category
                    break
                else:
                    print(f"Invalid category. Please select from: {', '.join(CFIValidator.CATEGORIES.keys())}")
        
        # Step 2: Select Group (if not provided)
        if not group:
            print("\nStep 2: Select Group (Second Character)")
            print(f"Description: {CFIValidator.POSITION_DESCRIPTIONS[2]}")
            for key, value in CFIValidator.GROUPS[category].items():
                print(f"  {key} - {value}")
            
            while True:
                group = input("\nEnter group code: ").upper()
                if group in CFIValidator.GROUPS[category]:
                    print(f"Selected: {group} - {CFIValidator.GROUPS[category][group]}")
                    cfi_code += group
                    break
                else:
                    print(f"Invalid group. Please select from: {', '.join(CFIValidator.GROUPS[category].keys())}")
        
        category_group = category + group
        
        # Continue with the remaining positions
        current_position = len(cfi_code) + 1
        
        # Steps 3-6: Select Attributes
        for position in range(current_position, 7):
            print(f"\nStep {position}: Select Attribute (Character {position})")
            print(f"Description: {CFIValidator.POSITION_DESCRIPTIONS[position]}")
            
            if category_group in CFIValidator.ATTRIBUTES and position in CFIValidator.ATTRIBUTES[category_group]:
                options = CFIValidator.ATTRIBUTES[category_group][position]
                for key, value in options.items():
                    print(f"  {key} - {value}")
                
                while True:
                    attr = input(f"\nEnter attribute {position} code: ").upper()
                    if attr in options or attr == 'X':
                        if attr in options:
                            print(f"Selected: {attr} - {options[attr]}")
                        else:
                            print("Selected: X - Not applicable/Not specified")
                        cfi_code += attr
                        break
                    else:
                        valid_options = list(options.keys())
                        if 'X' not in valid_options:
                            valid_options.append('X')
                        print(f"Invalid attribute. Please select from: {', '.join(valid_options)}")
            else:
                print("No specific attributes defined for this position.")
                print("  X - Not applicable/Not specified is recommended")
                valid_options = "X or any alphabetic character"
                
                while True:
                    attr = input(f"\nEnter attribute {position} code (or press Enter for 'X'): ").upper()
                    if not attr:
                        attr = 'X'
                        print("Selected: X - Not applicable/Not specified")
                    elif attr.isalpha():
                        if attr == 'X':
                            print("Selected: X - Not applicable/Not specified")
                        else:
                            print(f"Selected: {attr} - Custom attribute")
                    else:
                        print("Invalid attribute. Please enter an alphabetic character.")
                        continue
                    
                    cfi_code += attr
                    break
        
        # Validate the final code
        is_valid, message, positions_info = CFIValidator.validate(cfi_code)
        if is_valid:
            print(f"\nGenerated valid CFI code: {cfi_code}")
            return cfi_code
        else:
            print(f"\nWarning: Generated code {cfi_code} is not valid: {message}")
            print("Please try generation again.")
            return None


def display_cfi_details(cfi_code):
    """
    Display detailed information about a valid CFI code with enhanced position descriptions.
    
    Args:
        cfi_code (str): The validated CFI code
    """
    is_valid, message, positions_info = CFIValidator.validate(cfi_code)
    
    if not is_valid:
        print(f"\n✗ Invalid CFI code: {message}")
        return
    
    print(f"\nCFI Code: {cfi_code}")
    print("===================")
    print("ISO 10962 Classification of Financial Instruments")
    print("===================")
    
    for pos in range(1, 7):
        info = positions_info[pos]
        print(f"\nPosition {pos}: {info['value']}")
        print(f"Description: {info['description']}")
        print(f"Meaning: {info['meaning']}")
        
        # Show all possible options for this position
        if pos == 1:  # Category
            print("Possible options:")
            for key, value in CFIValidator.CATEGORIES.items():
                print(f"  {key} - {value}")
        elif pos == 2:  # Group
            category = cfi_code[0]
            print(f"Possible options for category {category}:")
            for key, value in CFIValidator.GROUPS[category].items():
                print(f"  {key} - {value}")
        else:  # Attributes
            category_group = cfi_code[0:2]
            if category_group in CFIValidator.ATTRIBUTES and pos in CFIValidator.ATTRIBUTES[category_group]:
                print(f"Possible options for position {pos}:")
                for key, value in CFIValidator.ATTRIBUTES[category_group][pos].items():
                    print(f"  {key} - {value}")
            else:
                print("No specific validation rules for this position.")

