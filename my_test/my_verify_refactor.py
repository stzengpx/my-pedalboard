import sys
import os

# Ensure current dir is in path
sys.path.append(os.getcwd())

print("Testing Dynamic Imports from fx_custom...")

try:
    import fx_custom
    print(f"✅ Imported fx_custom: {fx_custom}")
    
    # Test MyChorus
    if hasattr(fx_custom, 'MyChorus'):
        print("✅ Found MyChorus in fx_custom")
        chorus = fx_custom.MyChorus()
        print(f"   Instantiated: {chorus}")
    else:
        print("❌ MyChorus NOT found in fx_custom")
        
    # Test MyShifter
    if hasattr(fx_custom, 'MyShifter'):
        print("✅ Found MyShifter in fx_custom")
        shifter = fx_custom.MyShifter()
        print(f"   Instantiated: {shifter}")
    else:
        print("❌ MyShifter NOT found in fx_custom")
        
    print("\nNamespace Content:")
    print(dir(fx_custom))

except Exception as e:
    print(f"❌ Verification Failed: {e}")
    import traceback
    traceback.print_exc()
