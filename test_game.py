"""
BOMB DEFUSER GAME - TEST SCRIPT
===============================

PURPOSE: Quick test to verify all components are working correctly
AUTHOR: Bomb Defuser Game
VERSION: 1.0

DESCRIPTION:
Simple test script to validate that all game components can be imported
and initialized without errors. Use this to debug any import or setup issues.
"""

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    
    try:
        from PyQt5.QtWidgets import QApplication
        print("✓ PyQt5 available")
    except ImportError as e:
        print(f"✗ PyQt5 import error: {e}")
        return False
    
    try:
        from pygments import highlight
        print("✓ Pygments available")
    except ImportError as e:
        print(f"✗ Pygments import error: {e}")
        print("  Note: Game will use basic syntax highlighting")
    
    try:
        from bomb_defuser import BombDefuserGame
        print("✓ Main game module")
    except ImportError as e:
        print(f"✗ Main game import error: {e}")
        return False
    
    try:
        from game_controller import GameController
        print("✓ Game controller")
    except ImportError as e:
        print(f"✗ Game controller import error: {e}")
        return False
    
    try:
        from level_manager import LevelManager
        print("✓ Level manager")
    except ImportError as e:
        print(f"✗ Level manager import error: {e}")
        return False
    
    try:
        from bomb_widget import BombWidget
        print("✓ Bomb widget")
    except ImportError as e:
        print(f"✗ Bomb widget import error: {e}")
        return False
    
    try:
        from code_editor import CodeEditor
        print("✓ Code editor")
    except ImportError as e:
        print(f"✗ Code editor import error: {e}")
        return False
    
    return True

def test_level_data():
    """Test that level data is valid"""
    print("\nTesting level data...")
    
    try:
        from level_manager import LevelManager
        
        level_manager = LevelManager()
        validation_result = level_manager.validate_level_data_integrity()
        
        if validation_result['valid']:
            print(f"✓ All {validation_result['valid_levels']}/10 levels valid")
        else:
            print(f"✗ Level data issues found:")
            for issue in validation_result['issues']:
                print(f"  - {issue}")
                
        # Test first level specifically
        level_1 = level_manager.get_level(1)
        if level_1:
            print(f"✓ Level 1 loaded: {level_1['title']}")
        else:
            print("✗ Could not load Level 1")
            
        return validation_result['valid']
        
    except Exception as e:
        print(f"✗ Level data test error: {e}")
        return False

def test_basic_functionality():
    """Test basic game functionality without GUI"""
    print("\nTesting basic functionality...")
    
    try:
        from level_manager import LevelManager
        
        level_manager = LevelManager()
        
        # Test code validation
        level_1_data = level_manager.get_level(1)
        broken_code = level_1_data['broken_code']
        solution_code = level_1_data['solution_code']
        
        print(f"  Testing broken code validation...")
        broken_result = level_manager.validate_solution(1, broken_code)
        print(f"  Broken code valid: {broken_result['valid']} (should be False)")
        
        print(f"  Testing solution code validation...")
        solution_result = level_manager.validate_solution(1, solution_code)
        print(f"  Solution code valid: {solution_result['valid']} (should be True)")
        
        if not broken_result['valid'] and solution_result['valid']:
            print("✓ Code validation working correctly")
            return True
        else:
            print("✗ Code validation not working as expected")
            return False
            
    except Exception as e:
        print(f"✗ Basic functionality test error: {e}")
        return False

def main():
    """Run all tests"""
    print("BOMB DEFUSER GAME - COMPONENT TESTS")
    print("=" * 40)
    
    all_passed = True
    
    # Test imports
    if not test_imports():
        all_passed = False
    
    # Test level data
    if not test_level_data():
        all_passed = False
    
    # Test basic functionality
    if not test_basic_functionality():
        all_passed = False
    
    # Summary
    print("\n" + "=" * 40)
    if all_passed:
        print("✓ ALL TESTS PASSED - Game should work correctly!")
        print("\nTo start the game, run:")
        print("python bomb_defuser.py")
    else:
        print("✗ SOME TESTS FAILED - Check errors above")
        print("\nMake sure you have installed requirements:")
        print("pip install -r requirements.txt")
    
    print("=" * 40)

if __name__ == "__main__":
    main()