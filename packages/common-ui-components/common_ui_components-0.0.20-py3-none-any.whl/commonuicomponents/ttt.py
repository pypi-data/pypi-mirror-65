CAPTION = "TLabeledScale.Caption.TLabel"

print(style.lookup(CAPTION, "padx", default = "20 10"))

Label(self, text = caption).grid(row = 0, column = 0, padx = (20, 10), sticky = E)

self.__value = Label(self, anchor = E, text = from_, width = floor(log10(to)) + 1)
self.__value.grid(row = 0, column = 1, sticky = E)

self.__variable = IntVar()
self.__variable.set(from_)

Scale(
   self,
   command = self.onCommand,
   from_ = from_,
   length = 400,
   to = to,
   variable = self.__variable).grid(
      row = 0,
      column = 2,
      padx = 20,
      pady = 20)
