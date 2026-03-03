import os
import datetime

def main():
    print("🚀 开始自动发布流程...")
    print("📦 同步最新网页文件...")
    
    # 1. Add all changes
    os.system('git add .')
    
    # 2. Commit
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("Commiting changes...")
    os.system(f'git commit -m "Auto update {now}"')
    
    # 3. Push
    print("Pushing to GitHub...")
    os.system('git push origin main')
    
    print("✅ 发布成功！")

if __name__ == "__main__":
    main()
