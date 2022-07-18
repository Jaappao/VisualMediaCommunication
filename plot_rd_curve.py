import os
import cv2
import matplotlib.pyplot as plt

compression_rate = [1, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

converted_img_paths = []

class Plot():
    def __init__(self, path, type, compression_rate, psnr, bpp):
        self.path = path
        self.type = type
        self.compression_rate = compression_rate
        self.psnr = psnr
        self.bpp = bpp

    def __str__(self):
        return "{} {} {} {}".format(self.type ,str(self.compression_rate) ,str(self.psnr), str(self.bpp))
        # return self.type + str(self.compression_rate) + str(self.psnr) + str(self.bpp)
    
    def __repr__(self):
        return "{} {} {} {}".format(self.type ,str(self.compression_rate) ,str(self.psnr), str(self.bpp))

def main():
    files = [s for s in os.listdir('./') if '.png' in s]

    # 1: convert
    for file in files:
        targetName = file.split('.')[0]
        os.makedirs(targetName, exist_ok=True)
        
        img = cv2.imread(file)

        basename = os.path.dirname(os.path.abspath(file))
        print(basename)
        for i in compression_rate:
            img_save_path = os.path.join(basename, targetName, targetName+'_'+str(i)+'.jpg')
            if not os.path.exists(img_save_path):
                cv2.imwrite(img_save_path, img, [cv2.IMWRITE_JPEG_QUALITY, i])
                print("converted: " + img_save_path)
            converted_img_paths.append(img_save_path)


    # 2: caluculate PSNR and bpp
    plots = []

    for file in files:
        img = cv2.imread(file)
        
        targetName = file.split('.')[0]
        basename = os.path.dirname(os.path.abspath(file))        
        for i in compression_rate:
            img_save_path = os.path.join(basename, targetName, targetName+'_'+str(i)+'.jpg')
            img_converted = cv2.imread(img_save_path)

            psnr = cv2.PSNR(img, img_converted) # PSNR算出

            filebytes = os.path.getsize(img_save_path) # bytes
            height, width, ch = img.shape
            bpp = 8 * filebytes / (height*width)

            print(targetName+'_'+str(i)+'.jpg:')
            print("  PSNR: " + str(psnr)) 
            print("   BPP: " + str(bpp)) 

            plots.append(Plot(img_save_path, targetName, i, psnr, bpp))


    # 3: plot PSNR and bpp
    plt.figure(figsize=(10, 5))

    files.sort()
    print(files)

    for file in files:
        targetName = file.split('.')[0]

        target_plots = [s for s in plots if s.type == targetName]
        target_plots_psnr = [s.psnr for s in target_plots]
        target_plots_bpp = [s.bpp for s in target_plots]

        print(target_plots_psnr)
        print(target_plots_bpp)

        plt.plot(target_plots_bpp, target_plots_psnr, marker="+", label=targetName)
        

    plt.legend()
    # plt.show()
    plt.savefig("fig.pdf")


if __name__ == '__main__':
    main()