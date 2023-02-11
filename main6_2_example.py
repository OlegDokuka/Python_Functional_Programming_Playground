from typing import TypeVar, Generic, Iterator, List, Any
#
# T = TypeVar('T', bound="Employee", contravariant=True)
#
#
# class EmployeesOffice(Generic[T]):
#     def __init__(self, items: List[T]) -> None:
#         self.items = items
#
#     def __iter__(self) -> Iterator[T]:
#         return self.items.__iter__()
#
#     def put(self, value: T):
#         print(f"Added {value}")
#         self.items.append(value)
#
# class HeadOffice(EmployeesOffice["CEOS"]):
#     ...
#
#
# class Employee:
#     def __init__(self, name: str):
#         self._name = name
#
#     def name(self) -> str:
#         return self._name
#
#     def __str__(self):
#         return f"Employee {self._name}"
#
#
# class Manager(Employee):
#     def __init__(self, name: str):
#         super().__init__(f"Manager {name}")
#
#
# class CEOS(Manager):
#     def __init__(self, name: str):
#         super().__init__(f"CEOS {name}")
#
#
# def doing_for_employees(employees: EmployeesOffice[Employee]):
#     for v in employees:
#         print(v)
#
#
# def doing_for_manager(employees: EmployeesOffice[Manager]):
#     for v in employees:
#         print(v)




class CoffeeBean:
    def __init__(self, type: str):
        self.type = type

    def __str__(self):
        return self.type


class EthiopiaBean(CoffeeBean):
    def __init__(self):
        super().__init__("Ethiopia")


class BrazilianBean(CoffeeBean):
    def __init__(self):
        super().__init__("Brazilian")


class PremiumBrazilianBean(BrazilianBean):
    ...

T_Coffee_Beans = TypeVar("T_Coffee_Beans", bound=CoffeeBean, contravariant=True)


class CoffeeMachine(Generic[T_Coffee_Beans]):
    def __init__(self, type: str):
        self.type = type

    def put_beans(self, beans: T_Coffee_Beans):
        self.beans = beans

    def make_coffee(self):
        print(f"making coffee of beans {self.beans} in machine for {self.type}")


class GenericCoffeeCoffeeMachine(CoffeeMachine[CoffeeBean]):
    def __init__(self):
        super().__init__("generic")


class BrazilianCoffeeCoffeeMachine(CoffeeMachine[BrazilianBean]):
    def __init__(self):
        super().__init__("Brazilian")


class EthiopiaCoffeeCoffeeMachine(CoffeeMachine[EthiopiaBean]):
    def __init__(self):
        super().__init__("Ethiopia")





if __name__ == '__main__':
    # office: EmployeesOffice[Manager] = EmployeesOffice([Manager("michael")])
    # head_office = HeadOffice([CEOS("Mark")])
    #
    # doing_for_employees(head_office)

    machine: CoffeeMachine[EthiopiaBean] = GenericCoffeeCoffeeMachine()

    machine.put_beans(EthiopiaBean())
    machine.put_beans(BrazilianBean())
