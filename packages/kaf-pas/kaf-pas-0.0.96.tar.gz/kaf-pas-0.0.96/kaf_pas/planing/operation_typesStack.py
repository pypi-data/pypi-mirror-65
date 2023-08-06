import logging

from django.db import ProgrammingError

logger = logging.getLogger(__name__)


class Operation_typesStack:

    def get_first_item_of_tuple(self, tp):
        res, _ = tp
        return res

    def __init__(self):
        from kaf_pas.planing.models.operation_types import Operation_types
        from kaf_pas.planing.models.status_operation_types import Status_operation_typesManager
        from kaf_pas.planing.models.status_operation_types import Status_operation_types

        try:
            self.PRODUCTION_TASK = self.get_first_item_of_tuple(Operation_types.objects.update_or_create(code='PRD_TSK', defaults=dict(
                props=0,
                name='Задание на производство',
                editing=False,
                deliting=False,
            )))

            self.PRODUCTION_TASK_STATUSES = Status_operation_typesManager.make_statuses(
                opertype=self.PRODUCTION_TASK,
                status_map=[
                    dict(code='new', name='Новый', color='blue'),
                    dict(code='ready_2_start', name='Готов к запуску', color='green', props=Status_operation_types.props.blink),
                    dict(code='not_ready_2_start', name='К запуску не готов', color='red'),
                    dict(code='in_job', name='Просматривается', color='orange'),
                    dict(code='started', name='Запущен', color='blue'),
                    dict(code='started_partly', name='Запущен частично', color='blue', props=Status_operation_types.props.blink),
                    dict(code='transferred', name='Назначенный'),
                    dict(code='doing', name='Выполнен'),
                    dict(code='doing', name='Выполнен'),
                    dict(code='closed', name='Закрыт'),
                ]
            )

            self.PRODUCTION_DETAIL_TASK = self.get_first_item_of_tuple(Operation_types.objects.update_or_create(code='DETAIL_PRD_TSK', defaults=dict(
                props=0,
                name='Детализация Задания на производство',
                editing=False,
                deliting=False,
                parent=self.PRODUCTION_TASK
            )))

            self.PRODUCTION_DETAIL_TASK_STATUSES = Status_operation_typesManager.make_statuses(
                opertype=self.PRODUCTION_DETAIL_TASK,
                status_map=[
                    dict(code='new', name='Новый'),
                ]
            )

            self.LAUNCH_TASK = self.get_first_item_of_tuple(Operation_types.objects.update_or_create(code='LAUNCH_TSK', defaults=dict(
                props=0,
                name='Запуск задания на производство',
                editing=False,
                deliting=False,
                parent=self.PRODUCTION_TASK
            )))

            self.LAUNCH_TASK_STATUSES = Status_operation_typesManager.make_statuses(
                opertype=self.LAUNCH_TASK,
                status_map=[
                    dict(code='new', name='Новый'),
                ]
            )

            self.MADE_OPERATIONS_TASK = self.get_first_item_of_tuple(Operation_types.objects.update_or_create(code='MADE_OPRS_TSK', defaults=dict(
                props=0,
                name='Выполнение производственной операции',
                editing=False,
                deliting=False,
                parent=self.PRODUCTION_TASK
            )))

            self.MADE_OPERATIONS_STATUSES = Status_operation_typesManager.make_statuses(
                opertype=self.MADE_OPERATIONS_TASK,
                status_map=[
                    dict(code='new', name='Новый'),
                ]
            )

            self.RELEASE_TASK_PLUS = self.get_first_item_of_tuple(Operation_types.objects.update_or_create(code='RELEASE_TSK_PLS', defaults=dict(
                props=Operation_types.props.plus,
                name='Выпуск изделий',
                editing=False,
                deliting=False,
                parent=self.PRODUCTION_TASK
            )))

            self.RELEASE_TASK_PLUS_STATUSES = Status_operation_typesManager.make_statuses(
                opertype=self.RELEASE_TASK_PLUS,
                status_map=[
                    dict(code='new', name='Новый'),
                ]
            )

            self.RELEASE_TASK_MINUS = self.get_first_item_of_tuple(Operation_types.objects.update_or_create(code='RELEASE_TSK_MNS', defaults=dict(
                props=Operation_types.props.minus,
                name='Выпуск изделий',
                editing=False,
                deliting=False,
                parent=self.PRODUCTION_TASK
            )))

            self.RELEASE_TASK_MINUS_STATUSES = Status_operation_typesManager.make_statuses(
                opertype=self.RELEASE_TASK_MINUS,
                status_map=[
                    dict(code='new', name='Новый'),
                ]
            )

            self.CALC_TASKS = self.get_first_item_of_tuple(Operation_types.objects.update_or_create(code='CLC_TSK', defaults=dict(
                props=0,
                name='Учет',
                editing=False,
                deliting=False,
            )))

            self.CALC_TASKS_STATUSES = Status_operation_typesManager.make_statuses(
                opertype=self.CALC_TASKS,
                status_map=[
                    dict(code='new', name='Новый'),
                ]
            )

            self.POSTING_TASK = self.get_first_item_of_tuple(Operation_types.objects.update_or_create(code='PST_TSK', defaults=dict(
                props=0,
                name='Оприходование',
                editing=False,
                deliting=False,
                parent=self.CALC_TASKS
            )))

            self.POSTING_TASK_STATUSES = Status_operation_typesManager.make_statuses(
                opertype=self.POSTING_TASK,
                status_map=[
                    dict(code='new', name='Новый'),
                ]
            )

            self.POSTING_DETAIL_TASK = self.get_first_item_of_tuple(Operation_types.objects.update_or_create(code='DETAIL_PST_TSK', defaults=dict(
                props=Operation_types.props.plus,
                name='Детализация Оприходывания',
                editing=False,
                deliting=False,
                parent=self.CALC_TASKS
            )))

            self.POSTING_DETAIL_TASK_STATUSES = Status_operation_typesManager.make_statuses(
                opertype=self.POSTING_DETAIL_TASK,
                status_map=[
                    dict(code='new', name='Новый'),
                ]
            )

            self.WRITE_OFF_TASK = self.get_first_item_of_tuple(Operation_types.objects.update_or_create(code='WRT_OFF_TSK', defaults=dict(
                props=0,
                name='Списание',
                editing=False,
                deliting=False,
                parent=self.CALC_TASKS
            )))

            self.WRITE_OFF_TASK_STATUSES = Status_operation_typesManager.make_statuses(
                opertype=self.WRITE_OFF_TASK,
                status_map=[
                    dict(code='new', name='Новый'),
                ]
            )

            self.WRITE_DETAIL_OFF_TASK = self.get_first_item_of_tuple(Operation_types.objects.update_or_create(code='DETAIL_WRT_OFF_TSK', defaults=dict(
                props=Operation_types.props.minus,
                name='Детализация Списания',
                editing=False,
                deliting=False,
                parent=self.CALC_TASKS
            )))

            self.WRITE_DETAIL_OFF_TASK_STATUSES = Status_operation_typesManager.make_statuses(
                opertype=self.WRITE_DETAIL_OFF_TASK,
                status_map=[
                    dict(code='new', name='Новый'),
                ]
            )

            self.ROUTING_TASK = self.get_first_item_of_tuple(Operation_types.objects.update_or_create(code='RT_TSK', defaults=dict(
                props=0,
                name='Маршрутизация',
                editing=False,
                deliting=False,
            )))

            self.ROUTING_TASK_STATUSES = Status_operation_typesManager.make_statuses(
                opertype=self.ROUTING_TASK,
                status_map=[
                    dict(code='new', name='Новый'),
                ]
            )


        except ProgrammingError as ex:
            logger.warning(ex)
