import os
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, ID3NoHeaderError

def update_mp3_metadata(directory, mode):
    """
    根据文件名自动更新 MP3 文件的元数据（标题和作者）。
    
    模式说明：
    - 模式 1：文件名格式为 '<作者 - 标题>.mp3'
    - 模式 2：文件名格式为 '<标题 - 作者>.mp3'
    如果文件名中没有 '-', 则仅将文件名作为标题。

    :param directory: 包含 MP3 文件的目录路径
    :param mode: 模式选择 (1 或 2)
    """
    if mode not in [1, 2]:
        print("无效的模式！请选择模式 1 或模式 2。")
        return

    for filename in os.listdir(directory):
        if filename.endswith('.mp3'):
            filepath = os.path.join(directory, filename)
            # 去掉扩展名
            name_without_extension = filename.rsplit(".mp3", 1)[0]

            if " - " in name_without_extension:
                # 文件名包含 '-'
                if mode == 1:
                    # 模式 1: <作者 - 标题>
                    artist, title = name_without_extension.split(" - ", 1)
                elif mode == 2:
                    # 模式 2: <标题 - 作者>
                    title, artist = name_without_extension.split(" - ", 1)

                try:
                    # 处理元数据
                    try:
                        audio = EasyID3(filepath)
                    except ID3NoHeaderError:
                        audio = EasyID3()
                        audio.save(filepath)

                    audio['title'] = title
                    audio['artist'] = artist
                    audio.save()
                    print(f"元数据已更新: {filename} -> [艺术家: {artist}, 标题: {title}]")
                except Exception as e:
                    print(f"处理文件 {filename} 时出错: {e}")
            else:
                # 文件名不包含 '-', 仅使用文件名作为标题
                title = name_without_extension
                try:
                    try:
                        audio = EasyID3(filepath)
                    except ID3NoHeaderError:
                        audio = EasyID3()
                        audio.save(filepath)

                    audio['title'] = title
                    audio.save()
                    print(f"元数据已更新: {filename} -> [标题: {title}]")
                except Exception as e:
                    print(f"处理文件 {filename} 时出错: {e}")

# 使用示例
if __name__ == "__main__":
    directory = input("请输入MP3文件所在目录路径: ").strip()
    mode = int(input("请输入模式（1: <作者 - 标题>, 2: <标题 - 作者>): ").strip())
    update_mp3_metadata(directory, mode)
