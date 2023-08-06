#pragma once

#include <stdio.h>
#include <assert.h>
#include <stdint.h>

#ifdef _WIN32
    #define IGE_EXPORT __declspec(dllexport)
#else
    #define IGE_EXPORT
#endif


#ifdef NDEBUG
    #define LOG_VERBOSE(...)
    #define LOG_DEBUG(...)
    #define LOG(...)
    #define LOG_WARN(...)
    #define LOG_ERROR(...)
#else
    #if defined(__ANDROID__)
        #include <android/log.h>

        #define LOG_VERBOSE(...) __android_log_print(ANDROID_LOG_VERBOSE, "Social", __VA_ARGS__);
        #define LOG_DEBUG(...) __android_log_print(ANDROID_LOG_DEBUG, "Social", __VA_ARGS__);
        #define LOG(...) __android_log_print(ANDROID_LOG_INFO, "Social", __VA_ARGS__);
        #define LOG_WARN(...) __android_log_print(ANDROID_LOG_WARN, "Social", __VA_ARGS__);
        #define LOG_ERROR(...) __android_log_print(ANDROID_LOG_ERROR, "Social", __VA_ARGS__);
    #else
        void SocialLogMessage(const char* format, ...);

        #define LOG_VERBOSE(...) SocialLogMessage(__VA_ARGS__);
        #define LOG_DEBUG(...) SocialLogMessage(__VA_ARGS__);
        #define LOG(...) SocialLogMessage(__VA_ARGS__);
        #define LOG_WARN(...) SocialLogMessage(__VA_ARGS__);
        #define LOG_ERROR(...) SocialLogMessage(__VA_ARGS__);
    #endif
#endif

class IGE_EXPORT Social
{
public:    
	Social();
	~Social();
	void init();
	void release();
};
