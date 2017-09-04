#ifndef SIMPLE_H_INCLUDED
#define SIMPLE_H_INCLUDED

#ifdef __cplusplus
#define EXPORT extern "C" __declspec (dllexport)
#else
#define EXPORT __declspec (dllexport)
#endif // __cplusplus

#include <windows.h>

EXPORT  void wtmsb(double pp,int pc,int tth,double bp1,double bp5,double acc1,double acc2,double acc3);

#endif // SIMPLE_H_INCLUDED
