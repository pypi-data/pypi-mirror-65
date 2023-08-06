#include "unity_build.cpp"
#include <iostream>

const int size = 2;
int main()
{
    NonReplacingSampler S(size);
    for(int ii=0; ii<size+10; ii++)
        std::cout << S.next() << std::endl;
}
