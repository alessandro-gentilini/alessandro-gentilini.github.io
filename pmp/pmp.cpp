#include "opencv2/core/core.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/calib3d/calib3d.hpp"

#include <iostream>
#include <algorithm>


void to_homogeneous(const std::vector< cv::Point2f >& non_homogeneous, std::vector< cv::Point3f >& homogeneous )
{
    homogeneous.resize(non_homogeneous.size());
    for ( size_t i = 0; i < non_homogeneous.size(); i++ ) {
        homogeneous[i].x = non_homogeneous[i].x;
        homogeneous[i].y = non_homogeneous[i].y;
        homogeneous[i].z = 1.0;
    }
}

void from_homogeneous(const std::vector< cv::Point3f >& homogeneous, std::vector< cv::Point2f >& non_homogeneous )
{
    non_homogeneous.resize(homogeneous.size());
    for ( size_t i = 0; i < non_homogeneous.size(); i++ ) {
        non_homogeneous[i].x = homogeneous[i].x / homogeneous[i].z;
        non_homogeneous[i].y = homogeneous[i].y / homogeneous[i].z;
    }
}

void draw_cross(cv::Mat &img, const cv::Point center, float arm_length, const cv::Scalar &color, int thickness = 5 )
{
    cv::Point N(center - cv::Point(0, arm_length));
    cv::Point S(center + cv::Point(0, arm_length));
    cv::Point E(center + cv::Point(arm_length, 0));
    cv::Point W(center - cv::Point(arm_length, 0));
    cv::line(img, N, S, color, thickness);
    cv::line(img, E, W, color, thickness);
}

double measure_distance(const cv::Point2f& p1, const cv::Point2f& p2, const cv::Matx33f& GG)
{
    std::vector< cv::Point2f > ticks(2);
    ticks[0] = p1;
    ticks[1] = p2;
    std::vector< cv::Point3f > ticks_h;
    to_homogeneous(ticks, ticks_h);

    std::vector< cv::Point3f > world_ticks_h(2);
    for ( size_t i = 0; i < ticks_h.size(); i++ ) {
        world_ticks_h[i] = GG * ticks_h[i];
    }
    std::vector< cv::Point2f > world_ticks_back;
    from_homogeneous(world_ticks_h, world_ticks_back);

    return cv::norm(world_ticks_back[0] - world_ticks_back[1]);
}

int main(int, char**)
{
    printf("OpenCV: %s", cv::getBuildInformation().c_str());
    char cal_name[] = "cal.jpg";

    cv::Size patternsize(4,3); //number of centers
    cv::Mat cal = cv::imread(cal_name);//, cv::IMREAD_GRAYSCALE);
    std::vector<cv::Point2f> img_px; //this will be filled by the detected centers

    bool found = cv::findChessboardCorners( cal, patternsize, img_px, cv::CALIB_CB_ADAPTIVE_THRESH );

    double square_side_mm = 30;
    double scale = 10;


    std::vector< cv::Point2f > world_tenth_of_mm;

    std::cout << found << "\n";
    if(found){      
        // I need the first corner at top-left
        if(img_px.front().y > img_px.back().y){
            std::cout << "Reverse order\n";
            std::reverse(img_px.begin(),img_px.end());
        }
        for(size_t r=0;r<patternsize.height;r++){
            for(size_t c=0;c<patternsize.width;c++){
                world_tenth_of_mm.push_back(cv::Point2f(c*square_side_mm,r*square_side_mm));
                draw_cross(cal,img_px[r*patternsize.width+c],5,CV_RGB(255, 0, 0));
                std::ostringstream oss;
                oss << "("<<r<<","<<c<<")";
                cv::putText(cal, oss.str(), img_px[r*patternsize.width+c], cv::FONT_HERSHEY_PLAIN, 1, CV_RGB(0, 255, 0), 1);
            }
        }
    }

    cv::namedWindow( "Cal", cv::WINDOW_NORMAL );
    cv::imshow( "Cal", cal );
    cv::imwrite(std::string("Cal")+cal_name+".png", cal);
    

    char img_name[] = "quaderno.jpg";
    cv::Mat img = cv::imread(img_name);
    if(img.empty()){
        std::cerr << "Failure reading " << img_name << "\n";
        return 1;
    }
    std::cout << img.size() << "\n\n";



    // Here I estimate the homography that brings the world to the image.
    cv::Mat H = cv::findHomography(world_tenth_of_mm, img_px);
    std::cout << H << "\n\n";

    // To back-project the image points into the world I need the inverse of the homography.
    cv::Mat G = H.inv();
    std::cout << G << "\n\n";

    

    // I can rectify the image.
    cv::Mat warped;
    //cv::warpPerspective(img, warped, G, cv::Size(square_side_mm*scale*(patternsize.width+1), square_side_mm*scale*(patternsize.height+1)));
    cv::warpPerspective(img, warped, G, img.size());


    // {
    //     // Here I manually picked the pixels coordinates of ticks '0' and '1' in the slide rule,
    //     // in the world the distance between them is 10mm.
    //     cv::Point2f tick_0(2017, 1159);
    //     cv::Point2f tick_1(1949, 1143);
    //     // I measure the distance and I write it on the image.
    //     std::ostringstream oss;
    //     oss << measure_distance(tick_0, tick_1, G) / scale;
    //     cv::line(img, tick_0, tick_1, CV_RGB(0, 255, 0));
    //     cv::putText(img, oss.str(), (tick_0 + tick_1) / 2, cv::FONT_HERSHEY_PLAIN, 3, CV_RGB(0, 255, 0), 3);
    // }

    // {
    //     // Here I manually picked the pixels coordinates of ticks '11' and '12' in the slide rule,
    //     // in the world the distance between them is 10mm.
    //     cv::Point2f tick_11(1277, 988);
    //     cv::Point2f tick_12(1211, 973);
    //     // I measure the distance and I write it on the image.
    //     std::ostringstream oss;
    //     oss << measure_distance(tick_11, tick_12, G) / scale;
    //     cv::line(img, tick_11, tick_12, CV_RGB(0, 255, 0));
    //     cv::putText(img, oss.str(), (tick_11 + tick_12) / 2, cv::FONT_HERSHEY_PLAIN, 3, CV_RGB(0, 255, 0), 3);
    // }

    // // I draw the points used in the estimate of the homography.
    // draw_cross(img, TL, 40, CV_RGB(255, 0, 0));
    // draw_cross(img, TR, 40, CV_RGB(255, 0, 0));
    // draw_cross(img, BL, 40, CV_RGB(255, 0, 0));
    // draw_cross(img, BR, 40, CV_RGB(255, 0, 0));

    cv::namedWindow( "Input image", cv::WINDOW_NORMAL );
    cv::imshow( "Input image", img );
    cv::imwrite("img.png", img);

    cv::namedWindow( "Rectified image", cv::WINDOW_NORMAL );
    cv::imshow( "Rectified image", warped );
    cv::imwrite("warped.png", warped);

    cv::waitKey(0);

    return 0;
}