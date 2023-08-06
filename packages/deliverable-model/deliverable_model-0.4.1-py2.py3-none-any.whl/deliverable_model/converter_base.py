class ConverterBase:
    def __call__(self, *args, **kwargs):
        return self.call(*args, **kwargs)

    def call(self, *args, **kwargs):
        raise NotImplementedError

    def get_config(self) -> dict:
        return {}

    @classmethod
    def from_config(cls, config) -> "ConverterBase":
        return cls(**config)
