import os
import xml.etree.ElementTree as ET

def new_bounds(bndbox, name:str, org_frame: str, NEW_RESOLUTION: int):
    value = bndbox.find(name).text
    value = float(value) / float(org_frame) * NEW_RESOLUTION
    bndbox.find(name).text = str(value)
    return

if __name__ == '__main__':
    ANNOT_PATH = 'C:/Users/sapir/PycharmProjects/annotation_changer'
    PROJECT_NAME= 'new_annotation'
    NEW_RESOLUTION = 1024
    for file in os.listdir(ANNOT_PATH):
        if not file.endswith('.xml'):
            continue

        filelink = os.path.join(ANNOT_PATH, file)
        tree = ET.parse(filelink)
        root = tree.getroot()
        filename = root.find('filename')
        current_name = str(filename.text)

        frame_width= 0
        frame_height= 0
        for size in root.findall('size'):
            frame_width= size.find('width').text
            frame_height = size.find('height').text
            size.find('width').text = str(NEW_RESOLUTION)
            size.find('height').text = str(NEW_RESOLUTION)

        for bndbox in root.findall('.object/bndbox'):
            new_bounds(bndbox, 'xmin', frame_width, NEW_RESOLUTION)
            new_bounds(bndbox, 'ymin', frame_height, NEW_RESOLUTION)
            new_bounds(bndbox, 'xmax', frame_width, NEW_RESOLUTION)
            new_bounds(bndbox, 'ymax', frame_height, NEW_RESOLUTION)

        # create new name and save img name in <filename>
        new_name = current_name.replace('frame', PROJECT_NAME + '_')[:-4]
        new_img_name = new_name + ".png"
        filename.text = str(new_img_name)
        # write new annotation
        tree.write(os.path.join(ANNOT_PATH, new_name + ".xml"))