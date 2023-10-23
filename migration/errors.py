class MigrateError(Exception):
    def __init__(self, message):
        super().__init__(message)


class KubernetesError(MigrateError):
    pass


class AivenError(MigrateError):
    pass


class AivenUnauthenticated(AivenError):
    pass
