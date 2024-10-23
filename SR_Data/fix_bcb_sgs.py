import shutil
import os

def fix_bcb_sgs_file():
    # Create backup
    src = 'data/config/BCB_SGS.csv'
    backup = src + '.bak'
    if not os.path.exists(backup):
        shutil.copy2(src, backup)

    # Read the original content
    with open(src, 'r') as f:
        lines = f.readlines()

    # Fix the problematic line
    fixed_lines = []
    for line in lines:
        if 'Viagens_Desp' in line and 'SELIC' in line:
            # Split the merged line into two separate lines
            fixed_lines.append('Viagens_Desp,22742,1000000\n')
            fixed_lines.append('SELIC,432,1\n')
        else:
            fixed_lines.append(line)

    # Write the fixed content
    with open(src, 'w') as f:
        f.writelines(fixed_lines)

if __name__ == '__main__':
    fix_bcb_sgs_file()
    print("BCB_SGS.csv file has been fixed.")
