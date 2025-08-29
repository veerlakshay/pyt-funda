from unittest.mock import patch, MagicMock, Mock

#replace a func where it is looked up
with patch("app.service.time.time", return_value=123.0):
    ...

# A mock object
m = Mock()
m.process.return_value = "ok"
m.process("file.txt")
m.process.assert_called_once_with("file.txt")

# Magicmock handles magic methods (__enter__/__exit__/__len__/)
mm =MagicMock()
len(mm) #won't crash


# Important: patch where used, not where defined

patch("app.service.http_get")  # not "app.utils.http_get"

# spec/spec_set to avoid “green tests, broken reality”
real = SomeClient()
fake = Mock(spec=real)        # only real attrs allowed; missing methods -> AttributeError
# or use class: Mock(spec=SomeClient)
