#pragma once

#include <memory>

void CreateMyWindow();
void Sync();
void Finalize();

namespace pyxie
{
    class pyxieApplication;    
}

extern std::shared_ptr<pyxie::pyxieApplication> gApp;
