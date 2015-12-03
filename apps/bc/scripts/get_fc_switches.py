#!/usr/bin/env python3

from san_env import get_apps


def run():

    apps = get_apps()
    fc_SwitchConnection = apps.get_model(app_label='fc', model_name='SwitchConnection')
    bc_SwitchConnection = apps.get_model(app_label='bc', model_name='SwitchConnection')

    bc_SwitchConnection.objects.all().delete()
    for obj in fc_SwitchConnection.objects.all():
        print(obj)
        bc_SwitchConnection(
                name=obj.name, address=obj.address,
                enabled=obj.enabled, order=obj.order
            ).save()

    return


def main():
    run()


if __name__ == '__main__':
    main()
