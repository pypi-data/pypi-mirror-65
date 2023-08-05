#pragma once
#include <string>
#include <vector>

/* 0.0% - 100.0% */
using percent = double;


struct Sentence {
    std::wstring_view sentence;
    uint64_t bitmap = 0;
};

struct DecomposedSet {
    std::vector<std::wstring_view> intersection;
    std::vector<std::wstring_view> difference_ab;
    std::vector<std::wstring_view> difference_ba;
    DecomposedSet(std::vector<std::wstring_view> intersection, std::vector<std::wstring_view> difference_ab, std::vector<std::wstring_view> difference_ba)
        : intersection(std::move(intersection))
        , difference_ab(std::move(difference_ab))
        , difference_ba(std::move(difference_ba))
    {}
};

struct Affix {
    std::size_t prefix_len;
    std::size_t suffix_len;
};

namespace utils {

std::vector<std::wstring_view> splitSV(const std::wstring_view& str);

DecomposedSet set_decomposition(std::vector<std::wstring_view> a, std::vector<std::wstring_view> b);

std::size_t joined_size(const std::wstring_view& x);

std::size_t joined_size(const std::vector<std::wstring_view>& x);

std::wstring join(const std::vector<std::wstring_view>& sentence);

percent result_cutoff(double result, percent score_cutoff);

void trim(std::wstring& s);

void lower_case(std::wstring& s);

std::wstring default_process(std::wstring s);

Affix remove_common_affix(std::wstring_view& a, std::wstring_view& b);

void remove_common_affix(std::vector<std::wstring_view>& a, std::vector<std::wstring_view>& b);
}

inline uint64_t bitmap_create(const std::wstring_view& sentence) {
    uint64_t bitmap = 0;
    for (const unsigned int& letter : sentence) {
        uint8_t shift = (letter % 16) * 4;
        uint64_t bitmask = static_cast<uint64_t>(0b1111) << shift;
        if ((bitmap & bitmask) != bitmask) {
            bitmap += static_cast<uint64_t>(1) << shift;
        }
    }
    return bitmap;
}

inline uint64_t bitmap_create(const std::vector<std::wstring_view>& sentence) {
    //TODO missing whitespace
    uint64_t bitmap = 0;
    for (const auto & word : sentence) {
        for (const unsigned int& letter : word) {
            uint8_t shift = (letter % 16) * 4;
            uint64_t bitmask = static_cast<uint64_t>(0b1111) << shift;
            if ((bitmap & bitmask) != bitmask) {
                bitmap += static_cast<uint64_t>(1) << shift;
            }
        }
    }
    return bitmap;
}

inline uint8_t bitmap_check(uint64_t bitmap1, uint64_t bitmap2) {
    uint8_t result = 0;
    while (bitmap1 || bitmap2) {
        uint8_t val1 = bitmap1 & 0b1111;
        uint8_t val2 = bitmap2 & 0b1111;
        if (val1 > val2) {
            result += val1 - val2;
        } else {
            result += val2 - val1;
        }
        bitmap1 >>= 4;
        bitmap2 >>= 4;
    }
    return result;
}