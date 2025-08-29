#!/usr/bin/env python3
"""
BACKUP CURRENT STATE
Tạo backup trước khi phát triển admin features
"""

import os
import shutil
import time
import json

def create_system_backup():
    """Tạo backup toàn bộ hệ thống"""
    print("💾 CREATING SYSTEM BACKUP")
    print("=" * 30)
    print(f"⏰ Backup time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Tạo thư mục backup với timestamp
    timestamp = time.strftime('%Y%m%d_%H%M%S')
    backup_dir = f"/workspaces/Mentalhealth/backups/admin_dev_backup_{timestamp}"
    
    try:
        os.makedirs(backup_dir, exist_ok=True)
        print(f"📁 Backup directory: {backup_dir}")
        
        # Backup các file quan trọng
        critical_files = [
            "SOULFRIEND.py",
            "components/admin.py", 
            "pages/admin_panel.py",
            "components/ui.py",
            "components/scoring.py",
            "components/questionnaires.py"
        ]
        
        backed_up_files = []
        
        for file_path in critical_files:
            full_path = f"/workspaces/Mentalhealth/{file_path}"
            if os.path.exists(full_path):
                # Tạo thư mục con nếu cần
                backup_file_dir = os.path.dirname(f"{backup_dir}/{file_path}")
                os.makedirs(backup_file_dir, exist_ok=True)
                
                # Copy file
                shutil.copy2(full_path, f"{backup_dir}/{file_path}")
                backed_up_files.append(file_path)
                print(f"✅ Backed up: {file_path}")
            else:
                print(f"⚠️ File not found: {file_path}")
        
        # Backup toàn bộ thư mục components và pages
        for directory in ["components", "pages", "data"]:
            src_dir = f"/workspaces/Mentalhealth/{directory}"
            dst_dir = f"{backup_dir}/{directory}"
            
            if os.path.exists(src_dir):
                shutil.copytree(src_dir, dst_dir, dirs_exist_ok=True)
                print(f"✅ Backed up directory: {directory}")
        
        # Tạo backup metadata
        backup_info = {
            "backup_time": time.strftime('%Y-%m-%d %H:%M:%S'),
            "backup_reason": "Admin development preparation",
            "backed_up_files": backed_up_files,
            "backup_directory": backup_dir,
            "system_status": "Preparing for admin feature development"
        }
        
        with open(f"{backup_dir}/backup_info.json", 'w', encoding='utf-8') as f:
            json.dump(backup_info, f, indent=2, ensure_ascii=False)
        
        print(f"\n📋 Backup completed successfully!")
        print(f"📊 Files backed up: {len(backed_up_files)}")
        print(f"💾 Backup size: {get_directory_size(backup_dir):.2f} MB")
        
        return backup_dir
        
    except Exception as e:
        print(f"❌ Backup failed: {e}")
        return None

def get_directory_size(directory):
    """Tính kích thước thư mục"""
    total_size = 0
    try:
        for dirpath, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                total_size += os.path.getsize(filepath)
    except:
        pass
    return total_size / (1024 * 1024)  # Convert to MB

def verify_backup(backup_dir):
    """Kiểm tra tính toàn vẹn của backup"""
    print(f"\n🔍 VERIFYING BACKUP: {backup_dir}")
    print("=" * 40)
    
    if not os.path.exists(backup_dir):
        print("❌ Backup directory not found")
        return False
    
    # Kiểm tra các file quan trọng
    critical_files = [
        "SOULFRIEND.py",
        "components/admin.py",
        "pages/admin_panel.py",
        "backup_info.json"
    ]
    
    all_good = True
    for file_path in critical_files:
        full_path = f"{backup_dir}/{file_path}"
        if os.path.exists(full_path):
            size = os.path.getsize(full_path)
            print(f"✅ {file_path} ({size} bytes)")
        else:
            print(f"❌ Missing: {file_path}")
            all_good = False
    
    print(f"\n🎯 Backup Status: {'✅ VERIFIED' if all_good else '❌ INCOMPLETE'}")
    return all_good

def create_restore_script(backup_dir):
    """Tạo script restore"""
    restore_script = f"""#!/bin/bash
# RESTORE SCRIPT - Created {time.strftime('%Y-%m-%d %H:%M:%S')}
# Restore from backup: {backup_dir}

echo "🔄 RESTORING FROM BACKUP"
echo "======================="

# Stop any running processes
pkill -f streamlit

# Restore files
cp -r {backup_dir}/components/* /workspaces/Mentalhealth/components/
cp -r {backup_dir}/pages/* /workspaces/Mentalhealth/pages/
cp {backup_dir}/SOULFRIEND.py /workspaces/Mentalhealth/

echo "✅ Restore completed"
echo "🚀 You can now restart the application"
"""
    
    restore_file = f"{backup_dir}/restore.sh"
    with open(restore_file, 'w') as f:
        f.write(restore_script)
    
    os.chmod(restore_file, 0o755)
    print(f"📜 Restore script created: {restore_file}")

if __name__ == "__main__":
    print("🚀 ADMIN DEVELOPMENT BACKUP SYSTEM")
    print("=" * 40)
    
    # Tạo backup
    backup_dir = create_system_backup()
    
    if backup_dir:
        # Verify backup
        if verify_backup(backup_dir):
            # Tạo restore script
            create_restore_script(backup_dir)
            
            print(f"\n🎉 BACKUP PROCESS COMPLETED!")
            print("=" * 30)
            print(f"📁 Backup location: {backup_dir}")
            print("✅ System state preserved")
            print("🔄 Restore script available")
            print("\n🚀 READY TO START ADMIN DEVELOPMENT!")
        else:
            print("\n❌ BACKUP VERIFICATION FAILED!")
    else:
        print("\n❌ BACKUP CREATION FAILED!")
