#include "opencv2/core/core.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/calib3d/calib3d.hpp"

#include <iostream>


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
    char img_name[] = "single-view-metrology.jpg";
    cv::Mat img = cv::imread(img_name);
    if(img.empty()){
        std::cerr << "Failure reading " << img_name << "\n";
        return 1;
    }
    std::cout << img.size() << "\n\n";
    std::vector< cv::Point2f > world_tenth_of_mm;
    std::vector< cv::Point2f > img_px;

    // Here I manually picked the pixels coordinates of the corners of the A4 sheet.
    cv::Point2f TL(711, 64);
    cv::Point2f BL(317, 1429);
    cv::Point2f TR(1970, 175);
    cv::Point2f BR(1863, 1561);

    // This is the standard size of the A4 sheet:
    const int A4_w_mm = 210;
    const int A4_h_mm = 297;
    const int scale = 10;

    // Here I create the correspondences between the world point and the
    // image points.
    img_px.push_back(TL);
    world_tenth_of_mm.push_back(cv::Point2f(0.0, 0.0));

    img_px.push_back(TR);
    world_tenth_of_mm.push_back(cv::Point2f(A4_w_mm * scale, 0.0));

    img_px.push_back(BL);
    world_tenth_of_mm.push_back(cv::Point2f(0.0, A4_h_mm * scale));

    img_px.push_back(BR);
    world_tenth_of_mm.push_back(cv::Point2f(A4_w_mm * scale, A4_h_mm * scale));

    // Here I estimate the homography that brings the world to the image.
    cv::Mat H = cv::findHomography(world_tenth_of_mm, img_px);
    std::cout << H << "\n\n";

    // To back-project the image points into the world I need the inverse of the homography.
    cv::Mat G = H.inv();
    std::cout << G << "\n\n";

    

    // I can rectify the image.
    cv::Mat warped;
    cv::warpPerspective(img, warped, G, cv::Size(2600, 2200 * 297 / 210));


    {
        // Here I manually picked the pixels coordinates of ticks '0' and '1' in the slide rule,
        // in the world the distance between them is 10mm.
        cv::Point2f tick_0(2017, 1159);
        cv::Point2f tick_1(1949, 1143);
        // I measure the distance and I write it on the image.
        std::ostringstream oss;
        oss << measure_distance(tick_0, tick_1, G) / scale;
        cv::line(img, tick_0, tick_1, CV_RGB(0, 255, 0));
        cv::putText(img, oss.str(), (tick_0 + tick_1) / 2, cv::FONT_HERSHEY_PLAIN, 3, CV_RGB(0, 255, 0), 3);
    }

    {
        // Here I manually picked the pixels coordinates of ticks '11' and '12' in the slide rule,
        // in the world the distance between them is 10mm.
        cv::Point2f tick_11(1277, 988);
        cv::Point2f tick_12(1211, 973);
        // I measure the distance and I write it on the image.
        std::ostringstream oss;
        oss << measure_distance(tick_11, tick_12, G) / scale;
        cv::line(img, tick_11, tick_12, CV_RGB(0, 255, 0));
        cv::putText(img, oss.str(), (tick_11 + tick_12) / 2, cv::FONT_HERSHEY_PLAIN, 3, CV_RGB(0, 255, 0), 3);
    }

    // I draw the points used in the estimate of the homography.
    draw_cross(img, TL, 40, CV_RGB(255, 0, 0));
    draw_cross(img, TR, 40, CV_RGB(255, 0, 0));
    draw_cross(img, BL, 40, CV_RGB(255, 0, 0));
    draw_cross(img, BR, 40, CV_RGB(255, 0, 0));

    cv::namedWindow( "Input image", cv::WINDOW_NORMAL );
    cv::imshow( "Input image", img );
    cv::imwrite("img.png", img);

    cv::namedWindow( "Rectified image", cv::WINDOW_NORMAL );
    cv::imshow( "Rectified image", warped );
    cv::imwrite("warped.png", warped);

    cv::waitKey(0);

    return 0;
}